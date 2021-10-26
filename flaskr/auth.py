from flask import current_app
import functools
from types import MethodDescriptorType

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
from .forms import *
from datetime import datetime

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        db = get_db()
        db.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (email, generate_password_hash(password)),
        )
        db.commit()
        return redirect(url_for("auth.login"))
    current_app.logger.info('Register page opened, (with above data entered, if exists)(auth/register.html).')
    return render_template('auth/register.html', form=form)
    



@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.email.data
        password = form.password.data
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None or not check_password_hash(user['password'], password):
            error = 'Incorrect username or password.'
            current_app.logger.warning('Incorrect password entered.')

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            current_app.logger.info('Above user logged in.')
            return redirect(url_for('index'))
            

        flash(error)
    current_app.logger.info('Login page opened. (auth/login.html)')
    return render_template('auth/login.html', form=form)

@bp.route('/profile', methods=('GET', 'POST'))
def profile():
    db = get_db()
    booking = db.execute(
        'SELECT t.id, t.room_id, r.room_number, substr(t.from_time, 1) from_time, substr(t.to_time, 1) to_time from room_time t'
        ' join room r on t.room_id = r.id'
        ' where t.user_id = ? and t.to_time > datetime()',
        (g.user['id'],)).fetchone() 
    if booking is not None:
        date_string = dateString(booking['from_time'])
    else:
        date_string = None
    
    form = ChangePassword(request.form)
    if request.method == 'POST' and form.validate():
        username = form.email.data
        password = form.password.data
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
    


    def change_password():
        badge_list = []
        if form.validate_on_submit():
            if user(form.password):
                user.password = form.new_password.data
                db.session.add(user)
                db.session.commit()
                flash('Your password has been updated.')
                return redirect(url_for('index'))
            else:
                flash('Original password is invalid.')
        return render_template(
            'index',
            form=form,
            user=user,
            badge_list=badge_list)

    current_app.logger.info('Profile page opened. (auth/profile.html)')
    return render_template('auth/profile.html', booking=booking, date=date_string)
    
    



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
    session.clear()
    current_app.logger.info('User logged out.')
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            current_app.logger.warning('User not logged in, redirecting to "auth.login".')
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def dateString(date):
    if date is not None:
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return  datetime.strftime(date, '%A %d %B %Y')
    return date