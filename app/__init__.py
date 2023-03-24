"""
File: __init__.py
Description: This file creates and configures an instance of the Flask application.
"""

import os
from flask import Flask, g

def create_app():
    """
    Create and configure an instance of the Flask application.
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.cfg', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import search
    app.register_blueprint(search.bp)

    from . import pandas_database
    app.config['pandas_database'] = pandas_database.load_records()
    app.config['products'] = pandas_database.load_products(
        os.path.join(app.instance_path, 'products.csv')
    )

    return app
