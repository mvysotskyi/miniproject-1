"""
Recipes Blueprint.
"""

import re
from flask import Blueprint, render_template, request, current_app, g, session, flash, redirect

from app.image_parser import get_image
from app.pandas_access.ingresient_to_list import all_recipes, full_recipe
from app.db import get_db
from app.auth import login_required

bp = Blueprint('recepies', __name__, url_prefix='/recepies')

@bp.route('/')
def recepies():
    """
    Render recepies page by ingredients.

    Parameters:
    -----------
    ingredients: list
        List of ingredients.

    Returns:
    --------
    Found recepies page.
    """
    ingredients = request.args.get('ingredients')
    if not ingredients:
        flash('You did not choose any ingredients(press "+" button on the right to do so).')
        return redirect('/search')

    ingredients = ingredients.replace('flour', 'flmy').replace('"', '').strip("[]").split(',')

    recepies_dict = all_recipes(
        ingredients,
        current_app.config["_pp"],
        current_app.config["_final"],
        current_app.config["ingredients"]
    )

    return render_template('recepies.html', recepies=recepies_dict, logged = g.user is not None)

@bp.route('/recepie')
def recepie():
    """
    Render recepie page.
    
    Parameters:
    -----------
    id: int
        Recepie id.

    Returns:
    --------
    Recepie page.
    """
    recepie_id = request.args.get('id')
    if not recepie_id:
        return render_template('error.html', error_text='You did not choose any recepie.')

    liked = str(recepie_id) in g.user['liked'].split(',') if g.user else False

    _recipe = full_recipe([int(recepie_id)], current_app.config["_final"])[0]
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
    _recipe['id'] = recepie_id

    return render_template(
        'receipt.html', 
        recipe=_recipe,
        liked=liked,
        image_url=get_image(_recipe['id'], _recipe['name']),
        logged = g.user is not None
    )

@bp.post('/like')
@login_required
def like():
    """
    Post request to like the recipe(recepie_id) by user(user_id).
    If like already exists, it will be deleted.

    Parameters:
    -----------
    recepie_id: int

    Returns:
    --------
    'ok' if everything is ok.
    'error' if recepie_id is None or user_id is None or wrong.
    """
    recepie_id = str(request.form.get('recepie_id', None))
    user_id = session.get('user_id')

    if recepie_id is None or user_id is None:
        return 'error', 400

    db = get_db()

    liked = db.execute(f'SELECT liked FROM user WHERE id = {user_id}').fetchone()
    if not liked:
        return 'error', 400

    if not liked['liked']:
        liked = str(recepie_id)
    else:
        liked = set(liked['liked'].split(','))
        liked = ','.join(list(liked.symmetric_difference(set([recepie_id]))))

    db.execute(f'UPDATE user SET liked = "{liked}" WHERE id = {user_id}')
    db.commit()

    return 'ok', 200
