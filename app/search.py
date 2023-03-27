"""
Search blueprint.
"""

from flask import Blueprint, render_template, request, current_app, session, url_for, g
from app.auth import login_required

from pathlib import Path
import re

from app.ingresient_to_list import all_recipes, full_recipe
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


@bp.route('/recepies')
def recepies():
    '''
    Documentation.
    '''
    _ingredients = request.args.get('ingredients')
    try:
        if '[' in _ingredients:
            _ingredients = _ingredients[1:-1].replace('flour', 'flmy').replace('"', '').split(',')
        else:
            _ingredients = _ingredients.replace('flour', 'flmy').replace('"', '').split(',')
    except TypeError:
        return render_template('error.html', error_text='You did not choose any ingredients. '+\
        'Please, go back and choose ingredients you have'+\
        ' at home (press "+" button on the right to do so.)')
    _recepies = all_recipes(_ingredients, current_app.config["_pp"], current_app.config["_final"])
    _recepies = [item[1] for item in list(_recepies.items())]

    user_id = session.get('user_id')

    if user_id is None:
        header_path = Path(__file__).parent / "static/html_parts/header_unlogged.html"
    else:
        header_path = Path(__file__).parent / "static/html_parts/header_logged.html"

    with header_path.open('r', encoding='utf-8') as _f:
        _header = _f.read()
        return render_template('recepies.html', recepies=_recepies, header = _header)


@bp.route('/recepie')
def recepie():
    '''
    Documentation.
    '''
    recepie_id = [int(request.args.get('id'))]
    _recipe = full_recipe(recepie_id, current_app.config["_final"])[0]
    _recipe['steps'] = '. '.join(_recipe['steps'][2:-2].replace("'", '!').split("!, !")) + '.'
    _recipe['ingredients'] = ', '.join(_recipe['ingredients'][2:-2].split("', '"))
    _comp = re.compile(r'((?<=[\.\?!]\s)(\w+)|(^\w+))')
    def cap(_match):
        '''
        Capitalize every first letter of a sentence.
        '''
        return (_match.group().capitalize())
    _recipe['steps'] = _comp.sub(cap, _recipe['steps'])
    _recipe['description'] = _comp.sub(cap, _recipe['description'])

    user_id = session.get('user_id')

    if user_id is None:
        header_path = Path(__file__).parent / "static/html_parts/header_unlogged.html"
    else:
        header_path = Path(__file__).parent / "static/html_parts/header_logged.html"

    with header_path.open('r', encoding='utf-8') as _f:
        _header = _f.read()
        return render_template('receipt.html', recipe=_recipe, header = _header)

