"""
Search blueprint.
"""

from flask import Blueprint, render_template, request
from app.ingredient_show import request_names

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/livesearch', methods=["POST", "GET"])
def livesearch():
    '''
    Documentation.
    '''
    searchbox = request.form.get('text')
    res = request_names(searchbox)
    return res

@bp.route('/',methods=["POST", "GET"])
def index():
    '''
    Main page.
    '''
    return render_template('index.html')
