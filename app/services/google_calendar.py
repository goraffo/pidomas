from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
from datetime import datetime
from app import db

class GoogleCalendarService:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    CLIENT_SECRETS_FILE = 'client_secret.json'
    
    def __init__(self):
        self.credentials = None
        self.service = None
        
    def get_credentials(self):
        """Obtiene las credenciales de Google Calendar"""
        if self.credentials and self.credentials.valid:
            return self.credentials
            
        if self.credentials and self.credentials.expired and self.credentials.refresh_token:
            self.credentials.refresh(Request())
            return self.credentials
            
        flow = Flow.from_client_secrets_file(
            self.CLIENT_SECRETS_FILE,
            scopes=self.SCOPES,
            redirect_uri='http://localhost:5000/oauth2callback'
        )
        
        auth_url, _ = flow.authorization_url(prompt='consent')
        return auth_url
        
    def set_credentials(self, code):
        """Establece las credenciales usando el código de autorización"""
        flow = Flow.from_client_secrets_file(
            self.CLIENT_SECRETS_FILE,
            scopes=self.SCOPES,
            redirect_uri='http://localhost:5000/oauth2callback'
        )
        
        flow.fetch_token(code=code)
        self.credentials = flow.credentials
        self.service = build('calendar', 'v3', credentials=self.credentials)
        
    def create_event(self, event):
        """Crea un evento en Google Calendar"""
        if not self.service:
            raise Exception("Google Calendar service not initialized")
            
        google_event = event.to_google_calendar_event()
        created_event = self.service.events().insert(
            calendarId='primary',
            body=google_event
        ).execute()
        
        # Actualizar el evento local con el ID de Google Calendar
        event.google_calendar_id = created_event['id']
        db.session.commit()
        
        return created_event
        
    def update_event(self, event):
        """Actualiza un evento en Google Calendar"""
        if not self.service or not event.google_calendar_id:
            raise Exception("Google Calendar service not initialized or event not synced")
            
        google_event = event.to_google_calendar_event()
        updated_event = self.service.events().update(
            calendarId='primary',
            eventId=event.google_calendar_id,
            body=google_event
        ).execute()
        
        return updated_event
        
    def delete_event(self, event):
        """Elimina un evento de Google Calendar"""
        if not self.service or not event.google_calendar_id:
            raise Exception("Google Calendar service not initialized or event not synced")
            
        self.service.events().delete(
            calendarId='primary',
            eventId=event.google_calendar_id
        ).execute()
        
    def sync_event(self, event):
        """Sincroniza un evento con Google Calendar"""
        if not self.service:
            raise Exception("Google Calendar service not initialized")
            
        if not event.google_calendar_id:
            return self.create_event(event)
        else:
            return self.update_event(event)
            
    def get_event(self, google_calendar_id):
        """Obtiene un evento de Google Calendar"""
        if not self.service:
            raise Exception("Google Calendar service not initialized")
            
        return self.service.events().get(
            calendarId='primary',
            eventId=google_calendar_id
        ).execute()
        
    def list_events(self, time_min=None, time_max=None):
        """Lista eventos de Google Calendar"""
        if not self.service:
            raise Exception("Google Calendar service not initialized")
            
        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=time_min.isoformat() if time_min else None,
            timeMax=time_max.isoformat() if time_max else None,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', []) 