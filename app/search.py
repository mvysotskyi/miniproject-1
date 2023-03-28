"""
Search blueprint.
"""

from flask import Blueprint, render_template, request, session
from app.ingredient_show import request_names

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/',methods=["POST", "GET"])
def index():
    '''
    Main page.
    '''
    user_id = session.get('user_id')
    return render_template('search.html', logged = user_id is not None)

@bp.route('/livesearch', methods=["POST", "GET"])
def livesearch():
    """
    Live search.
    Returns a list of ingredients that match the searchbox.
    """
    searchbox = request.form.get('text')
    res = request_names(searchbox)
    return res
