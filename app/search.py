"""
Search blueprint.
"""

from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for
)

from app.auth import login_required

from app.db import get_db

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.get('/')
@login_required
def search_page():
    """
    Search page.
    GET: Render search page.
    """
    return render_template("search/search.html")

@bp.post('/')
@login_required
def search():
    """
    Search.
    POST: Search for an ingredient.
    """
    return "ingredient_name"
