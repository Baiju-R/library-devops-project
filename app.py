import os
import sys
import logging
from flask import Flask, g, session, redirect, render_template, request, jsonify, Response
from markupsafe import escape
from Misc.functions import *

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

app = Flask(__name__)
from werkzeug.middleware.proxy_fix import ProxyFix

# app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
app.secret_key = os.getenv("SECRET_KEY","devkey")

# Setting DAO Class
from Models.DAO import DAO

DAO = DAO(app)

# Registering blueprints
from routes.user import user_view
from routes.book import book_view
from routes.admin import admin_view

# Registering custom functions to be used within templates
app.jinja_env.globals.update(
    ago=ago,
    str=str,
)

app.register_blueprint(user_view)
app.register_blueprint(book_view)
app.register_blueprint(admin_view)

@app.route('/health')
def health_check():
	"""Health check endpoint for monitoring"""
	return jsonify({"status": "healthy", "service": "library-management-system"}), 200

@app.route('/testheaders')
def test_headers():
    from flask import request
    return str(dict(request.headers)) + "\nHost url: " + request.host_url


print("[INFO] App initialized successfully", file=sys.stdout, flush=True)

# Global error handler
@app.errorhandler(404)
def not_found(error):
	from flask import request
	print(f"[404] {request.url} {request.headers}", file=sys.stdout, flush=True)
	return "Not found: " + request.url, 404

@app.errorhandler(Exception)
def handle_error(error):
	error_msg = f"[EXCEPTION] {error}\n"
	import traceback
	tb_str = traceback.format_exc()
	print(error_msg, file=sys.stderr, flush=True)
	print(tb_str, file=sys.stderr, flush=True)
	# Also print to stdout so Gunicorn logs it
	print(error_msg, file=sys.stdout, flush=True)
	print(tb_str, file=sys.stdout, flush=True)
	return "Error: " + str(error), 500

# Also wrap before_request to debug
@app.before_request
def log_request():
	print(f"[REQUEST] {request.method} {request.path} from {request.remote_addr}", file=sys.stdout, flush=True)

@app.after_request
def log_response(response):
	print(f"[RESPONSE] {request.method} {request.path} -> {response.status_code}", file=sys.stdout, flush=True)
	return response