from flask import current_app, request
import functools
from types import MethodDescriptorType

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
from .forms import *

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        db = get_db()
        db.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (email, generate_password_hash(password)),
        )
        db.commit()
        return redirect(url_for("auth.login"))
    current_app.logger.info('Register page opened, (with above data entered, if exists)(auth/register.html). IP: ' + str(request.environ['REMOTE_ADDR']))
    return render_template('auth/register.html', form=form)
    



@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        username = form.email.data
        password = form.password.data
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None or not check_password_hash(user['password'], password):
            error = 'Incorrect username or password.'
            current_app.logger.warning('Incorrect password entered. IP: ' + str(request.environ['REMOTE_ADDR']))

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            current_app.logger.info(user['username'] + ' logged in. IP: ' + str(request.environ['REMOTE_ADDR']))
            return redirect(url_for('index'))
            

        flash(error, 'error form')
    current_app.logger.info('Login page opened. (auth/login.html) IP: ' + str(request.environ['REMOTE_ADDR']))
    return render_template('auth/login.html', form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    current_app.logger.info('User logged out. (auth/profile.html) USER: ' + g.user['username'] + ' IP: ' + str(request.environ['REMOTE_ADDR']))
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            current_app.logger.warning('User not logged in, redirecting to "auth.login". ' + str(request.environ['REMOTE_ADDR']))
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
