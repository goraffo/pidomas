from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from app.google_auth import get_flow, credentials_to_dict
from app.calendar_service import get_available_slots, create_appointment
from datetime import datetime, timedelta

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/calendar')
def calendar():
    if 'credentials' not in session:
        return render_template('calendar.html', authorized=False)
    
    # Obtener slots disponibles para la próxima semana
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)
    available_slots = get_available_slots(start_date, end_date)
    
    return render_template('calendar.html', 
                         authorized=True, 
                         available_slots=available_slots)

@calendar_bp.route('/calendar/slots')
def get_slots():
    if 'credentials' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    # Obtener fechas del query string
    try:
        start_date = datetime.fromisoformat(request.args.get('start_date'))
        end_date = datetime.fromisoformat(request.args.get('end_date'))
        duration = int(request.args.get('duration', 60))
    except (ValueError, TypeError):
        return jsonify({'error': 'Fechas inválidas'}), 400
    
    slots = get_available_slots(start_date, end_date, duration)
    if slots is None:
        return jsonify({'error': 'Error al obtener slots'}), 500
    
    return jsonify({
        'slots': [
            {
                'start': slot['start'].isoformat(),
                'end': slot['end'].isoformat()
            }
            for slot in slots
        ]
    })

@calendar_bp.route('/calendar/authorize')
def authorize():
    flow = get_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

@calendar_bp.route('/calendar/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = get_flow()
    flow.fetch_token(authorization_response=request.url)
    
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)
    
    return redirect(url_for('calendar.calendar'))

@calendar_bp.route('/calendar/schedule', methods=['POST'])
def schedule_appointment():
    if 'credentials' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        data = request.get_json()
        start_time = datetime.fromisoformat(data['start_time'])
        end_time = datetime.fromisoformat(data['end_time'])
        summary = data['summary']
        description = data.get('description', '')
        
        # Verificar que el slot esté disponible
        slots = get_available_slots(start_time, end_time)
        slot_available = any(
            slot['start'] == start_time and slot['end'] == end_time 
            for slot in slots
        )
        
        if not slot_available:
            return jsonify({'error': 'El horario seleccionado no está disponible'}), 400
        
        # Crear la cita
        appointment = create_appointment(
            summary=summary,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
        
        if appointment:
            return jsonify({
                'message': 'Cita agendada exitosamente',
                'appointment': appointment
            })
        else:
            return jsonify({'error': 'Error al crear la cita'}), 500
            
    except KeyError:
        return jsonify({'error': 'Datos incompletos'}), 400
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido'}), 400 