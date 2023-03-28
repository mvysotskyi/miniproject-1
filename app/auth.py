"""
Auth Blueprint.
"""

import re
import functools

from flask import Blueprint, g, redirect, render_template, request, session, url_for, current_app
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db
from app.pandas_access.ingresient_to_list import full_recipe

bp = Blueprint('auth', __name__, url_prefix='/auth')

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

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    Register a new user.
    Validates that the username is not already taken.
    Hashes the password for security.
    
    GET: Renders the register page.
    POST: Registers the user and redirects to the login page.

    POST request parameters:
        username: Username of the user.
        email: Email of the user.
        password: Password of the user.
    
    Returns:
        Renders the register page if the request method is GET.
        Error page if the request method is POST and some error occurs.
    """
    user_id = session.get('user_id')

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

        return render_template('error.html', error_text=error, logged=user_id is not None)

    return render_template('auth/register.html', logged=user_id is not None)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    Log in a registered user by adding the user id to the session.

    GET: Renders the login page.
    POST: Logs in the user and redirects to the search page.

    POST request parameters:
        email: Email of the user.
        password: Password of the user.

    Returns:
        Renders the login page if the request method is GET.
        Error page if the request method is POST and some error occurs.
    """
    user_id = session.get('user_id')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        error = None

        user = db.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()

        if user is None:
            error = errors["inv_email"]
        elif not check_password_hash(user['password'], password):
            error = errors["unc_password"]

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect("/search")

        return render_template('error.html', error_text=error, logged=False)

    return render_template('auth/login.html', logged=user_id is not None)

@bp.route('/logout')
def logout():
    """
    Clear the current session, including the stored user id.

    Returns:
        Redirects to the login page.
    """
    session.clear()
    return redirect(url_for('auth.login'))

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

@bp.route('/account')
def account():
    """
    Render current user account page.
    """
    if not g.user:
        return redirect(url_for('auth.login'))

    like_indexes = list(map(int, g.user['liked'].split(','))) if g.user['liked'] else []
    liked_recepies = full_recipe(like_indexes, current_app.config["_final"])
    liked_recepies = [item[1] for item in list(liked_recepies.items())]
    index_recepie = list(zip(like_indexes, liked_recepies))

    return render_template(
        'account.html',
        username=g.user['username'],
        logged = True,
        liked_recepies=index_recepie
    )
