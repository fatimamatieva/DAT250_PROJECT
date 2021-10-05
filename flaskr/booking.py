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
    return render_template('booking/booking.html')