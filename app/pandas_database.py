"""
Pandas database module.

This module contains functions to load data from csv files.
"""

import pandas as pd

def load_recipes(path: str):
    """
    Load recipes from csv file.
    """
    ...

def load_products(path: str):
    """
    Load products from csv file.
    """
    return pd.read_csv(path)["ingredients"]
