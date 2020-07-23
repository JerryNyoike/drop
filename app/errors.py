from flask import Blueprint, render_template, redirect, session


bp = Blueprint('errors', __name__, url_prefix='/')


@bp.errorhandler(404)
def page_not_found():
	return render_template('error_handler.html', page="Not Found", error=404, message="Page Not found"), 404