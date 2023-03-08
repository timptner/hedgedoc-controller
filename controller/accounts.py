from controller.authentication import login_required
from controller.database import get_database
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

blueprint = Blueprint('accounts', __name__, url_prefix='/accounts')


@blueprint.route('')
@login_required
def index():
    database = get_database()
    users = database.execute('SELECT username FROM users').fetchall()
    return render_template('accounts/index.html', users=users)
