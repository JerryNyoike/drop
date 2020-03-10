import pymysql.cursors
from flask import current_app, g
from flask.cli import with_appcontext, click

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(host=current_app.config['DB_HOST']
                               , user=current_app.config['DB_USER']
                               , password=current_app.config['DB_PASS']
                               , db=current_app.config['DB']
                               , cursorclass=current_app.config['CURSOR'])
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    cur = db.cursor()

    with current_app.open_resource('./schema.sql') as f:
        queries = f.read().decode('utf-8').replace('\n', ' ').replace('\t', ' ').split(';')
        for num, query in enumerate(queries):
            query = query.strip()
            if not query:
                continue
            cur.execute(query)
            db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database!")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
