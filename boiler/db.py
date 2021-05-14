import sqlite3

import click
from flask import current_app, g # g unique for each request. stores data that might be accessed by multiple functions during request.  Stored and re-used instead of new connection
# current_app b/c we used an app factory, there is no app object when writing rest of code.
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# close db and init_db_commands need to be registered in app instance.  Since using factory, the instance isn't vailable at that time.
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)