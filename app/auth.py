"""
Auth Blueprint.
"""

import functools
import re
from pathlib import Path

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
                print("User already registered.")
            else:
                return redirect(url_for("auth.login"))

        if user_id is None:
            header_path = Path(__file__).parent / "static/html_parts/header_unlogged.html"
        else:
            header_path = Path(__file__).parent / "static/html_parts/header_logged.html"

        with header_path.open('r', encoding='utf-8') as _f:
            _header = _f.read()
            return render_template('error.html', error_text=error, header = _header)


    if user_id is None:
        header_path = Path(__file__).parent / "static/html_parts/header_unlogged.html"
    else:
        header_path = Path(__file__).parent / "static/html_parts/header_logged.html"

    with header_path.open('r', encoding='utf-8') as _f:
        _header = _f.read()
        return render_template('auth/register.html', header = _header)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    Log in a registered user by adding the user id to the session.
    """
    user_id = session.get('user_id')
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

        if user_id is None:
            header_path = Path(__file__).parent / "static/html_parts/header_unlogged.html"
        else:
            header_path = Path(__file__).parent / "static/html_parts/header_logged.html"

        with header_path.open('r', encoding='utf-8') as _f:
            _header = _f.read()
            return render_template('error.html', error_text=error, header = _header)

    if user_id is None:
        header_path = Path(__file__).parent / "static/html_parts/header_unlogged.html"
    else:
        header_path = Path(__file__).parent / "static/html_parts/header_logged.html"

    with header_path.open('r', encoding='utf-8') as _f:
        _header = _f.read()
        return render_template('auth/login.html', header = _header)

@bp.route('/account')
def account():
    _username = g.user['username']
    header_path = Path(__file__).parent / "static/html_parts/header_logged.html"
    with header_path.open('r', encoding='utf-8') as _f:
        _header = _f.read()
        return render_template('account.html', username=_username, header = _header)


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
