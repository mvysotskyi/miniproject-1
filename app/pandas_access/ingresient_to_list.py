"""
This module contains the function that returns the list of ingredients.
"""

import pandas as pd

def all_recipes(ingredient_list, pp_recipes, final):
    """
    Retuns a dictionary with the recipes that contain all the ingredients.

    Parameters
    ----------
    ingredient_list : list
        A list of ingredients.

    Returns
    -------
    dict
        A dictionary with the recipes that contain all the ingredients.
    """
    ingredient_id_list = []
    pickle = pd.read_pickle('instance/ingr_map.pkl')
    search = pickle.groupby(by='replaced').mean(numeric_only=True)
    for ingredient in ingredient_list:
        ingredient_id = int(search.loc[ingredient,'id'])
        ingredient_id_list.append(ingredient_id)
    def func(row):
        row = row[1:-1]
        row = row.split(', ')
        row = [int(elem) for elem in row]
        for _id in ingredient_id_list: # or -> for _id in row
            if _id not in row: # or -> for _id in ingredient_id_list
                return False
        return True
    results = pp_recipes[pp_recipes['ingredient_ids'].apply(func)].head(15)
    dicti = {}
    final_id  = final.set_index('id')
    for elem in final_id.loc[results['id'], :].index:
        dicti[len(dicti)] = dict(final_id.loc[elem, ['name',
    'minutes',
    'calorie_level']]) | {'index': elem}
    return dicti

def full_recipe(id_list, final):
    """
    Returns a dictionary with the full recipe.

    Parameters
    ----------
    id_list : list
        A list of ids.

    Returns
    -------
    dict
        A dictionary with the full recipe.
    """
    dicti = {}
    prep = final[final['id'].isin(id_list)].set_index('id').loc[id_list, ['name',
    'minutes',
    'steps',
    'description',
    'ingredients',
    'calorie_level']]
    for _id in id_list:
        dicti[len(dicti)] = dict(prep.loc[_id,:])
    return dicti
