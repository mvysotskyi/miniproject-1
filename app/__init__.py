"""
File: __init__.py
Description: This file creates and configures an instance of the Flask application.
"""

import os
from flask import Flask

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

    # REMOVE THIS BLOCK
    # -----------------
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
