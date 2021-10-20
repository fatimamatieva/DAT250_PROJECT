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
    
    return render_template('booking/booking.html', rooms=rooms, date=date, today=today, time=['08'==time, '10'==time, '12'==time])

@bp.route("/booking/confirm/<int:room_id>", methods = ['GET','POST'])
@login_required
def confirm(room_id):
    booking_data = session['booking']
    print(booking_data['date'])
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
        db = get_db()
        db.execute(
            'INSERT INTO room_time (room_id, from_time, to_time, user_id)'
            ' VALUES (?, ?, ?, ?)',
            (room_id, date_time_from, date_time_to, 2))
        db.commit()
        flash(f'Booking confirmed')
        return redirect(url_for("index"))

    return render_template('booking/confirm.html', data=booking_data)


# @bp.route("/booking/confirm", methods = ['POST'])
# @login_required
# def confirm():
#     if request.is_json:
#         data = request.get_json()
#         print(data)

#         room_number = int(data['room_number'])
#         print(room_number)
#         print(type(room_number))
#         db = get_db()
#         room_id = db.execute(
#         'SELECT id FROM room'
#         ' WHERE room_number = ?',(room_number,)).fetchone()

#         print(room_id['id'])

#         date = data['date']
#         date = date[0:10]
#         time = data['time']

#         from_hours = time + ':00:00'
#         to_hours = str(int(time)+2) + ':00:00'
#         from_time = date + ' ' + from_hours
#         to_time = date + ' ' + to_hours

#         date_time_from = datetime.strptime(from_time, '%Y-%m-%d %H:%M:%S')
#         date_time_to = datetime.strptime(to_time, '%Y-%m-%d %H:%M:%S')

#         #TODO:  insert new booking into database
#         #       should the user have a limited amount of reservations?

#         db.execute(
#             'INSERT INTO room_time (room_id, from_time, to_time, user_id)'
#             ' VALUES (?, ?, ?, ?)',
#             (room_id['id'], date_time_from, date_time_to, 2))
#         db.commit()

#         response = {'message': 'Booking confirmed', 'code': 'SUCCESS'}

#         #escaping because of untrusted data --> Preventing XXS.
#         flash(f'Booking for room {escape(room_number)} confirmed')
#         return make_response(jsonify(response), 201)

#     response = {'message': 'Something want wrong', 'code': 'ERROR'}
#     return make_response(jsonify(response),400)

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
    'SELECT id, room_number FROM room r'
    ' WHERE not exists(SELECT * FROM room_time where room_id = r.id' 
    ' and from_time < ? and to_time > ?)'
    ' ORDER BY room_number',(date_time_to, date_time_from)).fetchall()

    if rooms is None:
        abort(404)
    return rooms   

