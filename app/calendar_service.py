from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
from app.google_auth import get_credentials

def get_calendar_service():
    credentials = get_credentials()
    if not credentials:
        return None
    
    return build('calendar', 'v3', credentials=credentials)

def get_available_slots(start_date, end_date, duration_minutes=60, timezone='America/Argentina/Buenos_Aires'):
    """
    Encuentra slots disponibles en el calendario entre dos fechas.
    
    Args:
        start_date (datetime): Fecha de inicio de la búsqueda
        end_date (datetime): Fecha de fin de la búsqueda
        duration_minutes (int): Duración de cada slot en minutos
        timezone (str): Zona horaria para la búsqueda
    
    Returns:
        list: Lista de slots disponibles en formato {start: datetime, end: datetime}
    """
    service = get_calendar_service()
    if not service:
        return None
    
    # Obtener eventos existentes
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_date.isoformat() + 'Z',
        timeMax=end_date.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    # Definir horario laboral (9:00 AM a 6:00 PM)
    business_start_hour = 9
    business_end_hour = 18
    
    # Generar todos los slots posibles
    available_slots = []
    current_date = start_date
    
    while current_date < end_date:
        # Solo considerar días de semana (0 = Lunes, 6 = Domingo)
        if current_date.weekday() < 5:  # Lunes a Viernes
            # Comenzar desde el horario laboral
            slot_start = current_date.replace(
                hour=business_start_hour, 
                minute=0, 
                second=0, 
                microsecond=0
            )
            
            while slot_start.hour < business_end_hour:
                slot_end = slot_start + timedelta(minutes=duration_minutes)
                
                # Verificar si el slot está disponible
                is_available = True
                for event in events:
                    event_start = datetime.fromisoformat(
                        event['start'].get('dateTime', event['start'].get('date'))
                    )
                    event_end = datetime.fromisoformat(
                        event['end'].get('dateTime', event['end'].get('date'))
                    )
                    
                    # Si hay superposición con algún evento, el slot no está disponible
                    if (slot_start < event_end and slot_end > event_start):
                        is_available = False
                        break
                
                if is_available:
                    available_slots.append({
                        'start': slot_start,
                        'end': slot_end
                    })
                
                slot_start += timedelta(minutes=duration_minutes)
        
        current_date += timedelta(days=1)
    
    return available_slots

def create_appointment(summary, description, start_time, end_time, timezone='America/Argentina/Buenos_Aires'):
    """
    Crea una cita en el calendario.
    """
    service = get_calendar_service()
    if not service:
        return None
    
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': timezone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 30},
            ],
        },
    }
    
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        return event
    except Exception as e:
        print(f"Error al crear cita: {e}")
        return None

def create_event(summary, description, start_time, end_time, timezone='America/Argentina/Buenos_Aires'):
    service = get_calendar_service()
    if not service:
        return None
    
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': timezone,
        },
    }
    
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        return event
    except Exception as e:
        print(f"Error al crear evento: {e}")
        return None

def list_events(time_min=None, time_max=None, max_results=10):
    service = get_calendar_service()
    if not service:
        return None
    
    if not time_min:
        time_min = datetime.utcnow().isoformat() + 'Z'
    if not time_max:
        time_max = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'
    
    try:
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])
    except Exception as e:
        print(f"Error al listar eventos: {e}")
        return None 