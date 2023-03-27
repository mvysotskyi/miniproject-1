"""
Recipes Blueprint.
"""

import re
from flask import Blueprint, render_template, request, current_app

from app.ingresient_to_list import all_recipes, full_recipe
from app.db import get_db

bp = Blueprint('recepies', __name__, url_prefix='/recepies')

@bp.route('/')
def recepies():
    """
    Documentation.
    """
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
    return render_template('recepies.html', recepies=_recepies)

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
    return render_template('receipt.html', recipe=_recipe)

@bp.post('/like')
def like():
    """
    Post request to like the recipe(recepie_id) by user(user_id).
    If like already exists, it will be deleted.
    """
    recepie_id = request.form.get('recepie_id', None)
    user_id = request.form.get('user_id', None)

    if recepie_id is None or user_id is None:
        return 'error', 400

    db = get_db()

    liked = db.execute(f'SELECT liked FROM user WHERE id = {user_id}').fetchone()
    if liked['liked'] is None:
        liked = str(recepie_id)
    else:
        liked = liked['liked'].split(',')
        if recepie_id in liked:
            liked.remove(recepie_id)

        liked = ','.join(liked + [recepie_id])

    db.execute(f'UPDATE user SET liked = "{liked}" WHERE id = {user_id}')
    db.commit()

    return 'ok', 200
