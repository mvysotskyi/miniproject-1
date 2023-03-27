"""
Script is used to make a csv file of all the ingredients in the recipes.
"""

import pandas as pd

df = pd.read_csv('../../instance/recipes.csv')

def make_list(string):
    """
    Converts a string of a list into a list.
    """
    return string[1:-1].split(',')

unique_values = set([value.strip("  '  ") for sublist in df['ingredients'] for value in make_list(sublist)])
unique_df = pd.DataFrame({'ingredients': list(unique_values)})

unique_df.to_csv('../../instance/products.csv', index=False)
