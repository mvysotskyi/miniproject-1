"""
Search blueprint.
"""

from flask import Blueprint, render_template, request, g
from app.pandas_access.ingredient_show import request_names

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/')
def search():
    """
    Render the search page.
    """
    return render_template('search.html', logged=g is not None)

@bp.post('/livesearch')
def livesearch():
    """
    Live search.
    Returns a list of ingredients that match the searchbox.

    Parameters:
    ----------
    searchbox: str
        The string to search for.

    Returns:
    -------
    res: list
        A list of ingredients that match the searchbox.
    """
    searchbox = request.form.get('text')
    res = request_names(searchbox)
    return res
