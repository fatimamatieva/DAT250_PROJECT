from sqlite3.dbapi2 import Date
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, make_response
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

from datetime import datetime

bp = Blueprint('booking', __name__)

@bp.route('/booking', methods=('GET', 'POST'))
#@login_required
def booking():
    rooms = []
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        rooms = get_rooms(date, time)
    return render_template('booking/booking.html', rooms=rooms)

@bp.route("/booking/confirm", methods = ['POST'])
#@login_required
def confirm():
    if request.is_json:
        data = request.get_json()
        print(data)
        room = data['room_number']
        #date = data['date']
        #time = data['time']
        #TODO:  insert new booking into database
        #       should the user have a limited amount of reservations?

        response = {'message': 'Booking confirmed', 'code': 'SUCCESS'}
        flash(f'Booking for room {room} confirmed')
        return make_response(jsonify(response), 201)
    response = {'message': 'Something want wrong', 'code': 'ERROR'}

    return make_response(jsonify(response),400)

#@bp.route('/booking/confirm/', methods=('GET', 'POST'))
#@login_required
#def confirm():
#    if request.method == 'POST':
#        room = request.form['room']
#        date = request.form['date']
#        time = request.form['time']
#        comments = request.form['comments']
#        db = get_db()
#        db.execute(
#            'INSERT INTO room_time (room_id, from_time, to_time, Comments, user_id)'
#            ' VALUES (?, ?, ?, ?, ?)',
#            (date, room, time, comments, g.user['id'])
#        )
#        db.commit()
#        flash("Booking successful")
#        return redirect(url_for('blog.index'))
#
#    return render_template('booking/confirm.html')

# def get_room(date, time, room):
    
#     room = get_db().execute(
#         'SELECT RoomName, Date, Time'
#         ' FROM rooms'
#         ' WHERE Date = ? AND Time = ? AND RoomName= ?',
#         (date,time,room,)
#     ).fetchone()

#     if room is None:
#         abort(404)
#     return room  

def get_rooms(date, time):
#    rooms = get_db().execute(
#       'SELECT RoomName, Date, Time'
 #       ' FROM rooms'
 #       ' WHERE Date = ? AND Time = ?',
 #       (date,time,)
 #   ).fetchone()

    from_hours = time + ':00:00'
    to_hours = str(int(time)+2) + ':00:00'
    from_time = date + ' ' + from_hours
    to_time = date + ' ' + to_hours

    date_time_from = datetime.strptime(from_time, '%Y-%m-%d %H:%M:%S')
    date_time_to = datetime.strptime(to_time, '%Y-%m-%d %H:%M:%S')

    db = get_db()

    rooms = db.execute(
    'SELECT id, room_number from room r'
    ' where not exists(SELECT * FROM room_time where room_id = r.id' 
    ' and from_time < ? and to_time > ?)'
    ' ORDER BY room_number',(date_time_from, date_time_to)).fetchall()

    if rooms is None:
        abort(404)
    return rooms   

