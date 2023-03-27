"""
Recipes Blueprint.
"""

import re
from flask import Blueprint, render_template, request, current_app

from app.ingresient_to_list import all_recipes, full_recipe

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
