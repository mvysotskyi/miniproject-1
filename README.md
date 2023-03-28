# miniproject-1
Miniproject No. 1. UCook

# Short Description
This is a simple recipe app that allows users to search for recipes based on ingredients. The app also allows users to save recipes to their favorites list. Users have the option to create an account and login to save their favorites list.

# Installation

- Clone the repository
- Make virtual environment
```bash
python3 -m venv venv
```
- Install requirements
```bash
pip install -r requirements.txt
```
- Initialize the database
```bash
flask --app app init-user-table
```
- Run the app
```bash
flask --app app run
```

## About ```instance``` folder

The ```instance``` have to be not included in the repository. It contains the following files that is changed like database, config, and other.


# Documentation

- **__init__.py**
This file is the main file of the app. It contains the app factory and the app instance. It also contains the blueprints for the app.

- **db.py**
This file contains the database instance and the database models.

- **auth.py**
Very simple authentication system. It contains the login and logout routes, register route, and some useful functions.

- **recipes.py**
This file contains the routes for the recipes. The route for recepie page and page with recepies search results.
Also have API for recepies likes.

- **search.py**
This file contains the routes for the search. The route for search page and api for ingredients search.(unsed for livesearch)

## Other folders

- **static** - contains static files like css, js, images, etc.
- **templates** - contains html templates
- **sql** - contains sql files for database creation
- **pandas_access** - contains python modules for working with our Pandas dataset
