"""
Database connection and close functions.
"""

import click
import sqlite3

from flask import current_app, g

def get_db():
    """
    Get a database connection.
    :return: sqlite3.Connection
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """
    Close the database connection.
    :param e: Exception
    :return: None
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    """
    Register the database functions with the Flask app.
    :param app: Flask
    :return: None
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_user_table_command)

def init_user_table():
    """
    Create the user table.
    :return: None
    """
    db = get_db()

    with current_app.open_resource('sql/user.sql') as sql_file:
        db.executescript(sql_file.read().decode('utf8'))

@click.command('init-user-table')
def init_user_table_command():
    """
    Clear the existing data and create new tables.
    :return: None
    """
    init_user_table()
    click.echo('Initialized the user table.')
