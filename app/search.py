"""
Search blueprint.
"""

from flask import Blueprint, render_template, request, session, url_for
from pathlib import Path
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
    user_id = session.get('user_id')

    if user_id is None:
        header_path = Path(__file__).parent / "static/html_parts/header_unlogged.html"
    else:
        header_path = Path(__file__).parent / "static/html_parts/header_logged.html"

    with header_path.open('r', encoding='utf-8') as _f:
        _header = _f.read()
        return render_template('index.html', header = _header)





