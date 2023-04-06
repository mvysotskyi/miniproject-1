"""
This module contains the function that returns the list of ingredients.
"""

def all_recipes(ingredient_list, pp_recipes, final, ingredients):
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
    ingredients = ingredients.groupby(by='replaced').mean(numeric_only=True)
    ingredient_id_set = set(map(int, ingredients.loc[ingredient_list, 'id']))

    def filter_func(row):
        row = {int(elem) for elem in row[1:-1].split(', ')}
        return row.issuperset(ingredient_id_set)

    results = pp_recipes[pp_recipes['ingredient_ids'].apply(filter_func)]['id'].head(12)

    final_id  = final.set_index('id')
    return final_id.loc[results, ['name', 'minutes', 'calorie_level']].to_dict('index')

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
