from flask import Blueprint, g, session, redirect, render_template, request
from markupsafe import escape
from Controllers.UserManager import UserManager
from Controllers.BookManager import BookManager

book_view = Blueprint('book_routes', __name__, template_folder='/templates')

# Managers will be initialized on first route access (lazy initialization)
book_manager = None
user_manager = None

def _init_managers():
	"""Initialize managers with DAO on first use (avoids circular import)"""
	global book_manager, user_manager
	if book_manager is None:
		from app import DAO
		book_manager = BookManager(DAO)
		user_manager = UserManager(DAO)
	return book_manager, user_manager


@book_view.route('/books/test', methods=['GET'])
def test_route():
	"""Test route to debug"""
	from flask import request
	return f"Host URL: {request.host_url} | Host: {request.host} | Headers: {dict(request.headers)}", 200


def get_user_reserved_books():
	"""Get list of book IDs reserved by current user"""
	bm, um = _init_managers()
	user_books = []
	if um.user.isLoggedIn():
		try:
			reserved = bm.getReserverdBooksByUser(user_id=um.user.uid())
			if reserved and reserved.get('user_books'):
				user_books = [str(b).strip() for b in reserved['user_books'].split(',') if b.strip()]
		except Exception as e:
			print(f"[WARNING] Could not fetch reserved books: {e}")
	return user_books


@book_view.route('/books/', methods=['GET'], strict_slashes=False)
@book_view.route('/books/<int:book_id>', methods=['GET'])
def books_list(book_id=None):
	"""Display books list or single book details"""
	print(f"[BOOKS_LIST] Called with book_id={book_id}", flush=True)
	try:
		bm, um = _init_managers()
		print(f"[BOOKS_LIST] Managers initialized", flush=True)
		um.user.set_session(session, g)
		user_books = get_user_reserved_books()
		print(f"[BOOKS_LIST] User books count: {len(user_books)}", flush=True)
		
		# Single book view
		if book_id:
			book = bm.getBook(book_id)
			if not book:
				return render_template('books.html', error="Book not found", g=g, user_books=user_books, books=[])
			return render_template("book_view.html", books=book, g=g, user_books=user_books)
		
		# List all available books
		books = bm.list(availability=1)
		if not books:
			books = []
		print(f"[BOOKS_LIST] Books count: {len(books)}", flush=True)
		
		return render_template("books.html", books=books, g=g, user_books=user_books)
	
	except Exception as e:
		print(f"[ERROR] /books failed: {e}", flush=True)
		import traceback
		traceback.print_exc()
		return render_template("books.html", error="Error loading books", g=g, user_books=[], books=[])


@book_view.route('/books/add/<int:book_id>', methods=['GET'])
def reserve_book(book_id):
	"""Reserve a book for the logged-in user"""
	try:
		bm, um = _init_managers()
		
		# Check login
		if not um.user.isLoggedIn():
			return redirect('/signin')
		
		user_id = um.user.uid()
		if not user_id or user_id == "err":
			return redirect('/signin')
		
		# Reserve the book
		bm.reserve(user_id, book_id)
		
		um.user.set_session(session, g)
		user_books = get_user_reserved_books()
		books = bm.list(availability=1)
		if not books:
			books = []
		
		return render_template("books.html", msg="Book reserved successfully", books=books, g=g, user_books=user_books)
	
	except Exception as e:
		print(f"[ERROR] /books/add/{book_id} failed: {e}")
		import traceback
		traceback.print_exc()
		bm, um = _init_managers()
		um.user.set_session(session, g)
		user_books = get_user_reserved_books()
		books = bm.list(availability=1)
		if not books:
			books = []
		return render_template("books.html", error=f"Failed to reserve book", books=books, g=g, user_books=user_books)


@book_view.route('/books/search', methods=['GET'])
def books_search():
	"""Search for books by keyword"""
	try:
		bm, um = _init_managers()
		um.user.set_session(session, g)
		user_books = get_user_reserved_books()
		
		keyword = request.args.get('keyword', '').strip()
		if not keyword:
			return redirect('/books')
		
		results = bm.search(keyword, availability=1)
		if not results:
			results = []
		
		return render_template("books.html", books=results, count=len(results), 
							   search=True, keyword=escape(keyword), g=g, user_books=user_books)
	
	except Exception as e:
		print(f"[ERROR] /books/search failed: {e}")
		import traceback
		traceback.print_exc()
		bm, um = _init_managers()
		um.user.set_session(session, g)
		user_books = get_user_reserved_books()
		return render_template("books.html", error="Search failed", g=g, user_books=user_books, books=[])
