"""
File: __init__.py
Description: This file creates and configures an instance of the Flask application.
"""

import os
from flask import Flask, g

import pandas as pd

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

    app.config["_raw"] = pd.read_csv('instance/RAW_recipes.csv')
    app.config["_pp"] = pd.read_csv('instance/PP_recipes.csv')
    app.config["_final"] = app.config["_raw"].merge(app.config["_pp"],left_on='id',right_on='id')

    return app
