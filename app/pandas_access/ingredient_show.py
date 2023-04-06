"""
This module contains the function that returns the list of ingredients.
"""

import re

def request_names(request, ingr_map):
    """
    Returns a list of ingredients that match the request.

    Parameters
    ----------
    request : str
        The request to be matched.

    Returns
    -------
    dict
        A dictionary with the matched ingredients.
    """
    a = ingr_map.copy()
    a['replaced'].replace('flmy','flour',inplace=True)
    all_items = ','.join(list(set(a['replaced'])))
    a.set_index('raw_ingr',inplace=True)
    all_items = ',' +all_items
    all_items = all_items + ','
    results = re.findall(f',[ \w]*{request}[A-Za-z]*[ \w]*,', all_items)
    results = [elem[1:-1] for elem in results]
    results.sort(key = lambda x: len(x))
    return {i: results[i] for i in range(min(8,len(results)))}
