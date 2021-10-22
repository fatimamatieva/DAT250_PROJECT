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

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
    #    username = form.username.data
        email = form.email.data
        password = form.password.data
        db = get_db()
        db.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (email, generate_password_hash(password)),
        )
        db.commit()
        return redirect(url_for("auth.login"))
    current_app.logger.info('Register page opened, (with above data entered, if exists)(auth/register_test.html).')
    return render_template('auth/register_test.html', form=form)
    
# def register():
#     form = RegistrationForm(request.form)
#     if request.method == 'POST' and form.validate():
#     #    username = form.username.data
#         email = form.email.data
#         password = form.password.data
#         db = get_db()
#         error = None

#         if not email:
#             error = 'Email is required.'
#         elif not password:
#             error = 'Password is required.'

#         if error is None:
#             try:
#                 db.execute(
#                     "INSERT INTO user (username, password) VALUES (?, ?)",
#                     (email, generate_password_hash(password)),
#                 )
#                 db.commit()
#             except db.IntegrityError:
#                 error = f"User {email} is already registered."
#             else:
#                 return redirect(url_for("auth.login"))
        

#         flash(error)

#     return render_template('auth/register.html', form=form)
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         db = get_db()
#         error = None

#         if not username:
#             error = 'Username is required.'
#         elif not password:
#             error = 'Password is required.'

#         if error is None:
#             try:
#                 db.execute(
#                     "INSERT INTO user (username, password) VALUES (?, ?)",
#                     (username, generate_password_hash(password)),
#                 )
#                 db.commit()
#             except db.IntegrityError:
#                 error = f"User {username} is already registered."
#             else:
#                 return redirect(url_for("auth.login"))
        

#         flash(error)

#     return render_template('auth/register.html')

# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
#         db.session.add(user)
#         db.session.commit()
#         flash(f'Your account has been created! You can now log in.', 'success')
#         return redirect(url_for('home'))
#     return render_template('register.html', title='Register', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
     #   username = form.username.data
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
    current_app.logger.info('Login page opened. (auth/login_test.html)')
    return render_template('auth/login_test.html', form=form)
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         db = get_db()
#         error = None
#         user = db.execute(
#             'SELECT * FROM user WHERE username = ?', (username,)
#         ).fetchone()

#         if user is None:
#             error = 'Incorrect username.'
#         elif not check_password_hash(user['password'], password):
#             error = 'Incorrect password.'

#         if error is None:
#             session.clear()
#             session['user_id'] = user['id']
#             return redirect(url_for('index'))

#         flash(error)

#     return render_template('auth/login.html')
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.email.data == 'admin@blog.com' and form.password.data == 'password':
#             flash(f'You have been logged in!', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful. Please check username and password', 'danger')
#     return render_template('login.html', title='Login', form=form)

@bp.route('/profile', methods=('GET', 'POST'))
def profile():
    db = get_db()
    booking = db.execute(
        'SELECT t.id, t.room_id, r.room_number, substr(t.from_time, 1) from_time, substr(t.to_time, 1) to_time from room_time t'
        ' join room r on t.room_id = r.id'
        ' where t.user_id = ? and t.to_time > datetime()',
        (g.user['id'],)).fetchone()

#    if booking is not None:
#        db.execute(
 #           'DELETE from room_time where id = ?',
  #          (booking['id'],))
  #      db.commit()





    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    current_app.logger.info('Profile page opened. (auth/profile.html)')
    return render_template('auth/profile.html', booking=booking)



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

