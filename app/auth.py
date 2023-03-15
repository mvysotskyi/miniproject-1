"""
Auth Blueprint.
"""

import functools
import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

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

    return render_template('auth/register.html')

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
            return redirect("/")

        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """
    Clear the current session, including the stored user id.
    """
    session.clear()
    return redirect(url_for('auth.login'))

# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))

#         return view(**kwargs)

#     return wrapped_view

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
