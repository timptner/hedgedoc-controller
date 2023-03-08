import click
import functools

from controller.database import get_database
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

blueprint = Blueprint('auth', __name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@blueprint.cli.command('register')
@click.argument('username')
@click.argument('password')
def register(username: str, password: str):
    """Register a new user."""
    database = get_database()
    username = username.lower()
    try:
        database.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        database.commit()
    except database.IntegrityError:
        click.echo(f"User '{username}' is already registered.")
    else:
        click.echo(f"New user '{username}' was created.")


@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_database().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()


@blueprint.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']

        database = get_database()
        error = None

        user = database.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('accounts.index'))

        flash(error, 'is-danger')

    return render_template('auth/login.html')


@blueprint.route('/logout')
@login_required
def logout():
    session.clear()
    flash("You are logged out.", 'is-info')
    return redirect(url_for('auth.login'))
