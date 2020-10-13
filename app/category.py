from flask import Blueprint, current_app, make_response, request, render_template, url_for
from markupsafe import escape
from . import db


bp = Blueprint('category', __name__, url_prefix='/category')


@bp.route('<category>', methods=['GET', 'POST'])
def category(category):
    if request.method == 'POST':
        request_info = request.get_json()
        limit = request.args.get('limit', 30)
        skip = request.args.get('skip', 0)

        category = ' '.join(escape(category).split('_')).capitalize()
        query = '''SELECT (BIN_TO_UUID(beat.beat_id)) beat_id, beat.name, beat.category, beat.beat_file, beat.lease_price, 
        beat.selling_price, beat.upload_date, (BIN_TO_UUID(producer.producer_id)) producer_id, producer.name producer FROM 
        beat INNER JOIN producer ON beat.producer_id=producer.producer_id WHERE beat.category = "{}"'''.format(category)
        
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute(query)
        beats = cur.fetchall()
        if not beats:
            return make_response({'status': 0, 'message': 'No beats found for this category'}, 404)

        # return the beats
        return make_response({'status': 1, 'message': 'Beats fetched successfully','beats': beats}, 200)

    crumbs = [
        {"name": "Discover", "url": url_for('routes.discover'), "active": "true"}
    ]
    page = ' '.join(escape(category).split('_')).capitalize()
    return render_template('category.html', page=page, crumbs=crumbs), 200


@bp.route('categories', methods = ['GET'])
def fetch_categories():
    query = 'SELECT DISTINCT category FROM beat_category';

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute(query) 
    categories = cur.fetchall()

    if not categories:
        return make_response({"status": 0, "message": "No categories Found"}, 404)

    return make_response({"status": 1, "message": "categories Found", "categories": categories}, 200)
