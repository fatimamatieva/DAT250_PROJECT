from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('booking', __name__)

@bp.route('/booking', methods=('GET', 'POST'))
def booking():
    rooms = []
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        rooms = get_rooms(date, time)
    return render_template('booking/booking.html', rooms=rooms)

@bp.route('/booking/confirm/', methods=('GET', 'POST'))
#@login_required
def confirm():
    if request.method == 'POST':
        room = request.form['room']
        date = request.form['date']
        time = request.form['time']
        comments = request.form['time']
        db = get_db()
        db.execute(
            'INSERT INTO room (RoomName, Date, Time, Comments, UserID)'
            ' VALUES (?, ?, ?, ?)',
            (room, date, time, comments, g.user['id'])
        )
        db.commit()
        flash("Booking successful")
        return redirect(url_for('blog.index'))
    return render_template('booking/confirm.html')

def get_room(date, time, room):
    room = get_db().execute(
        'SELECT RoomName, Date, Time'
        ' FROM rooms'
        ' WHERE Date = ? AND Time = ? AND RoomName= ?',
        (date,time,room,)
    ).fetchone()

    if room is None:
        abort(404)
    return room  

def get_rooms(date, time):
    rooms = get_db().execute(
        'SELECT RoomName, Date, Time'
        ' FROM rooms'
        ' WHERE Date = ? AND Time = ?',
        (date,time,)
    ).fetchone()

    if rooms is None:
        abort(404)
    return rooms   

