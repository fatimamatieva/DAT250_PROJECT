from sqlite3.dbapi2 import Date
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, make_response, escape,session
)
from flask import sessions
from flask.sessions import NullSession
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

from datetime import datetime

bp = Blueprint('booking', __name__)

@bp.route('/booking', methods=('GET', 'POST'))
@login_required
def booking():
    rooms = []
    today = datetime.now().strftime("%Y-%m-%d")
    date = None
    time = None
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        rooms = get_rooms(date, time)
        session['booking'] = {
            'date': date,
            'time': time
        }
    context = {
        'rooms': rooms,
        'date': date,
        'today': today,
        'time': ['08'==time, '10'==time, '12'==time]
    }
    return render_template('booking/booking.html', **context)

@bp.route("/booking/confirm/<int:room_id>", methods = ['GET','POST'])
@login_required
def confirm(room_id):
    room_number = get_room(room_id)
    session['booking']['room'] = room_number
    booking_data = session['booking']

    if request.method == 'POST':
        date = booking_data['date']
        date = date[0:10]
        time = booking_data['time']

        from_hours = time + ':00:00'
        to_hours = str(int(time)+2) + ':00:00'
        from_time = date + ' ' + from_hours
        to_time = date + ' ' + to_hours

        date_time_from = datetime.strptime(from_time, '%Y-%m-%d %H:%M:%S')
        date_time_to = datetime.strptime(to_time, '%Y-%m-%d %H:%M:%S')

        if date_time_to < datetime.now():
            flash(f'You cannot book back in time')
            return redirect(url_for("booking"))

        db = get_db()
        db.execute(
            'INSERT INTO room_time (room_id, from_time, to_time, user_id)'
            ' SELECT id, ?, ?, ?'
            ' FROM room r'
            ' WHERE id = ?'
            ' and not exists(SELECT * FROM room_time where room_id = r.id' 
            ' and from_time < ? and to_time > ?)'
            ' and not exists(SELECT * FROM room_time where user_id = ?' 
            ' and to_time > datetime())',
            (date_time_from, date_time_to, g.user['id'], room_id, date_time_to, date_time_from, g.user['id']))
        db.commit()

        booking = db.execute(
            'SELECT user_id FROM room_time where room_id = ?'
            ' and from_time = ? and to_time = ?',
            (room_id, date_time_from, date_time_to)).fetchone()


        if booking is None:
            flash(f'You already have a booking')

        elif booking['user_id'] == g.user['id']:
            flash(f'Booking for room {escape(room_number)} confirmed')
        else:
            flash(f'Room {escape(room_number)} is already booked') 

        return redirect(url_for("index"))

    return render_template('booking/confirm.html', data=booking_data)


@bp.route("/booking/cancel", methods=('POST',))
def cancel():
    flash('Booking canceled')
    return redirect(url_for('index'))


def get_rooms(date, time):
    from_hours = time + ':00:00'
    to_hours = str(int(time)+2) + ':00:00'
    from_time = date + ' ' + from_hours
    to_time = date + ' ' + to_hours

    date_time_from = datetime.strptime(from_time, '%Y-%m-%d %H:%M:%S')
    date_time_to = datetime.strptime(to_time, '%Y-%m-%d %H:%M:%S')

    db = get_db()

    rooms = db.execute(
    'SELECT id, room_number FROM room r'
    ' WHERE not exists(SELECT * FROM room_time where room_id = r.id' 
    ' and from_time < ? and to_time > ?)'
    ' ORDER BY room_number',(date_time_to, date_time_from)).fetchall()

    if rooms is None:
        abort(404)
    return rooms   

def get_room(id):
    db = get_db()
    room_number = db.execute(
    'SELECT room_number FROM room'
    ' WHERE id = ?',(id,)).fetchone()

    if room_number is None:
        abort(404)
    return room_number['room_number']  
