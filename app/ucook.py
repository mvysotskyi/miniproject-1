import pandas as pd
import regex as re
import functools
import re
from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db

from ingresient_to_list import all_recipes, full_recipe
from ingredient_show import request_names


app = Flask(__name__)
bp = Blueprint('auth', __name__, url_prefix='/auth')
app.register_blueprint(bp)

errors = {
    'inv_password': 'Password must be at least 6 characters long, \
contain at least one uppercase letter, one lowercase letter, \
one number, and one special character.',
    'unc_password': 'Password is incorrect.',
    'inv_email': 'Email is invalid.',
    'inv_username': 'Username is invalid.',
    'req_password': 'Password is required.',
    'req_email': 'Email is required.',
    'req_username': 'Username is required.'
}



@app.route('/',methods=["POST", "GET"])
def index():
    '''
    Main page.
    '''
    return render_template('index.html')

@app.route('/livesearch',methods=["POST", "GET"])
def livesearch():
    '''
    Documentation.
    '''
    searchbox = request.form.get('text')
    res = request_names(searchbox)
    return res

@app.route('/recepies')
def recepies():
    '''
    Documentation.
    '''
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
    _recepies = all_recipes(_ingredients, _pp, _final)
    _recepies = [item[1] for item in list(_recepies.items())]
    return render_template('recepies.html', recepies=_recepies)

@app.route('/recepie')
def recepie():
    '''
    Documentation.
    '''
    recepie_id = [int(request.args.get('id'))]
    _recipe = full_recipe(recepie_id, _final)[0]
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

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    Register a new user.
    Validates that the username is not already taken.
    Hashes the password for security.
    :return: None
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        error = None

        if not username:
            error = errors["req_username"]
        elif not password:
            error = errors["req_password"]

        # Password validation
        r_p = re.compile('^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')
        if not r_p.match(password):
            error = errors["inv_password"]

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (email, username, password) VALUES (?, ?, ?)",
                    (email, username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    Log in a registered user by adding the user id to the session.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = errors["inv_email"]
        elif not check_password_hash(user['password'], password):
            error = errors["unc_password"]

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect("/search")

        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """
    Clear the current session, including the stored user id.
    """
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    """
    View decorator that redirects anonymous users to the login page.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """
    If a user id is stored in the session, load the user object from
    the database into ``g.user``.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

if __name__ == '__main__':
    app.run(debug=True)
