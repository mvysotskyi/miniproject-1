"""
This script will take the raw and preprocessed csv files and merge them into one csv file.
"""

import pandas as pd

raw = pd.read_csv('RAW_recipes.csv')
pp = pd.read_csv('PP_recipes.csv')

final = raw.merge(pp, left_on='id', right_on='id')
final.to_csv('../../instance/recipes.csv', index=False)
