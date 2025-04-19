from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.routes import bp
from app.models import Appointment
from app import db

@bp.route('/events')
@login_required
def list_events():
    appointments = Appointment.query.all()
    return render_template('events/list.html', appointments=appointments)

@bp.route('/events/create', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        appointment = Appointment(
            user_id=current_user.id,
            advisor_id=request.form.get('advisor_id'),
            start_time=request.form.get('start_time'),
            end_time=request.form.get('end_time')
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Cita creada exitosamente', 'success')
        return redirect(url_for('main.list_events'))
    return render_template('events/create.html')

@bp.route('/events/<int:id>')
@login_required
def view_event(id):
    appointment = Appointment.query.get_or_404(id)
    return render_template('events/view.html', appointment=appointment) 