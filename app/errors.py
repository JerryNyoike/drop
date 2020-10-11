from flask import Blueprint, render_template, redirect, session
from werkzeug.exceptions import HTTPException
from flask_wtf.csrf import CSRFError

bp = Blueprint('errors', __name__, url_prefix='/')


@bp.errorhandler(HTTPException)
def error_handler(e):
    return render_template("error_handler.html", page="Error", error=e.description, message=e.name), e.code


@bp.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template("error_handler.html", page="Error", error=e.description, message=e.name), 401