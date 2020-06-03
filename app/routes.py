from flask import Blueprint, render_template, redirect, session


bp = Blueprint('routes', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def index():
	return render_template('index.html', page="Home"), 200


@bp.route('/explore', methods=['GET'])
def explore():
	return render_template('explore.html', page="Explore"), 200


@bp.route('/about', methods=['GET'])
def about():
	return render_template('about.html', page="About"), 200


@bp.route('/produce', methods=['GET'])
def produce():
	return render_template('produce.html', page="Produce"), 200


@bp.route('/contacts', methods=['GET'])
def contacts():
	return render_template('contacts.html', page="Contacts"), 200


@bp.route('/cart', methods=['GET'])
def cart():
	return render_template('cart.html', page="Cart"), 200