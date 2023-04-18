"""
File: __init__.py
Description: This file creates and configures an instance of the Flask application.
"""

import os
from flask import Flask, g, render_template

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

    from . import recepies
    app.register_blueprint(recepies.bp)

    # Load resources from bucket
    BUCKET_NAME = app.config["BUCKET_NAME"]

    app.config["_pp"] = pd.read_csv(f"gs://{BUCKET_NAME}/PP_recipes.csv", encoding="utf-8")
    app.config["_final"] = pd.read_csv(f"gs://{BUCKET_NAME}/recipes.csv", encoding="utf-8")
    app.config["ingredients"] = pd.read_pickle(f"gs://{BUCKET_NAME}/ingr_map.pkl")

    @app.route('/')
    def index():
        """
        Main page.
        """
        return render_template(
            'index.html', 
            random_recepies = app.config["_final"].sample(6).to_dict('records'),
            logged = g.user is not None
        )

    return app
