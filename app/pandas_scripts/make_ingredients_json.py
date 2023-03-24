"""
Script is used to make a csv file of all the ingredients in the recipes.
"""

import json
import pandas as pd

df = pd.read_csv('../../instance/recipes.csv')

def make_list(string):
    """
    Converts a string of a list into a list.
    """
    return string[1:-1].split(',')

unique_values = frozenset([value for sublist in df['ingredients'] for value in make_list(sublist)])

with open('../../instance/ingredients.json', 'w', encoding="utf-8") as f:
    json.dump(list(unique_values), f)
