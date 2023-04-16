"""
Module to parse images from food.com by name and id of the recipe.
"""

import requests
from bs4 import BeautifulSoup

from app.db import get_db

def get_image(recipe_id, recipe_name):
    """
    Get image from food.com by name and id of the recipe.
    :param recipe_id: int
    :param recipe_name: str
    :return: str
    """
    db = get_db()
    image = db.execute(
        'SELECT image_url FROM images WHERE recipe = ?',
        (recipe_id,)
    ).fetchone()

    if image is None:
        return parse_image(recipe_id, recipe_name)

    return image['image_url']

def parse_image(recipe_id, recipe_name):
    """
    Parse image from food.com by name and id of the recipe.
    :param recipe_id: int
    :param recipe_name: str
    :return: str
    """
    recipe_name = '-'.join(recipe_name.split(' '))

    url = f'https://www.food.com/recipe/{recipe_name}-{recipe_id}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    image = soup.find('img', {'style': '--aspect-ratio: 5/4'})
    if image is None:
        return ''

    image = image['srcset'].split(' ')[0]

    if 'recipe-default-images' in image:
        return ''

    if not image.startswith('http'):
        image = 'https:' + image

    db = get_db()
    db.execute(
        'INSERT INTO images (recipe, image_url) VALUES (?, ?)',
        (recipe_id, image)
    )
    db.commit()

    return image
