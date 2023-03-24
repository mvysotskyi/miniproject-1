"""
Search blueprint.
"""

from flask import Blueprint, render_template, request, current_app
from app.auth import login_required

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.get('/')
@login_required
def search_page():
    """
    Search page.
    GET: Render search page.
    """
    return render_template("search/search.html")

@bp.get('/product')
@login_required
def search_product():
    """
    Search product.
    Returns a list of 15 first products that match the search token.
    GET: Search for product. If product is found, return its full name.
    """
    token = request.args.get('value')
    if token is None:
        return "[]"

    iser = current_app.config['products']
    return iser[iser.str.contains(token, case=False)].head(15).to_json(orient='records')
