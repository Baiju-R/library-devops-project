from flask import Blueprint, g, session, redirect, render_template, request, jsonify, Response, flash
from markupsafe import escape
from functools import wraps
from Misc.functions import *

from Controllers.UserManager import UserManager

user_view = Blueprint('user_routes', __name__, template_folder='/templates')

# Lazy initialization to avoid circular import
user_manager = None

def _init_manager():
	"""Initialize user manager with DAO on first use (avoids circular import)"""
	global user_manager
	if user_manager is None:
		from app import DAO
		user_manager = UserManager(DAO)
	return user_manager

# Wrapper decorators that use lazy-initialized manager
def login_required_lazy(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		um = _init_manager()
		if not um.user.isLoggedIn():
			return redirect("/signin")
		return f(*args, **kwargs)
	return decorated_function

def redirect_if_login_lazy(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		um = _init_manager()
		if um.user.isLoggedIn():
			return redirect("/")
		return f(*args, **kwargs)
	return decorated_function


@user_view.route('/', methods=['GET'])
def home():
	g.bg = 1
	um = _init_manager()
	um.user.set_session(session, g)
	print(g.user)
	return render_template('home.html', g=g)


@user_view.route('/signin', methods=['GET', 'POST'])
@redirect_if_login_lazy
def signin():
	um = _init_manager()
	if request.method == 'POST':
		_form = request.form
		email = str(_form["email"])
		password = str(_form["password"])

		if len(email)<1 or len(password)<1:
			return render_template('signin.html', error="Email and password are required")

		d = um.signin(email, hash(password))

		if d and len(d)>0:
			session['user'] = int(d['id'])
			return redirect("/")

		return render_template('signin.html', error="Email or password incorrect")

	return render_template('signin.html')


@user_view.route('/signup', methods=['GET', 'POST'])
@redirect_if_login_lazy
def signup():
	um = _init_manager()
	if request.method == 'POST':
		name = request.form.get('name')
		email = request.form.get('email')
		password = request.form.get('password')

		if len(name) < 1 or len(email)<1 or len(password)<1:
			return render_template('signup.html', error="All fields are required")

		new_user = um.signup(name, email, hash(password))

		if new_user == "already_exists":
			return render_template('signup.html', error="User already exists with this email")

		return render_template('signup.html', msg = "You've been registered!")

	return render_template('signup.html')


@user_view.route('/signout/', methods=['GET'])
@login_required_lazy
def signout():
	um = _init_manager()
	um.signout()
	return redirect("/", code=302)


@user_view.route('/user/', methods=['GET'], strict_slashes=False)
@login_required_lazy
def show_user(id=None):
	um = _init_manager()
	um.user.set_session(session, g)
	
	if id is None:
		id = int(um.user.uid())

	d = um.get(id)
	mybooks = um.getBooksList(id)

	return render_template("profile.html", user=d, books=mybooks, g=g)


@user_view.route('/user', methods=['POST'])
@login_required_lazy
def update():
	um = _init_manager()
	um.user.set_session(session, g)
	
	_form = request.form
	name = str(_form["name"])
	email = str(_form["email"])
	password = str(_form["password"])
	bio = str(_form["bio"])

	um.update(name, email, hash(password), bio, um.user.uid())

	flash('Your info has been updated!')
	return redirect("/user/")

@user_view.route('/testheaders')
def test_headers():
    from flask import request
    return str(dict(request.headers))
