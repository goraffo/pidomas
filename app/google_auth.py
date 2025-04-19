<<<<<<< HEAD
from flask import session, redirect, url_for
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de OAuth 2.0
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_flow():
    return Flow.from_client_config(
        client_config={
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI]
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

def get_credentials():
    if 'credentials' not in session:
        return None
    
    credentials = Credentials(
        **session['credentials']
    )
    
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        session['credentials'] = credentials_to_dict(credentials)
    
    return credentials

def credentials_to_dict(credentials):
=======
import os
import secrets
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from flask import current_app

# Configuración de OAuth 2.0
CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_google_auth_url():
    """Genera la URL de autorización de Google OAuth2."""
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=current_app.config['GOOGLE_REDIRECT_URI']
    )
    
    # Generar un estado aleatorio para prevenir CSRF
    state = secrets.token_urlsafe(16)
    
    # Generar la URL de autorización
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        state=state
    )
    
    return auth_url, state

def get_google_token(code):
    """Obtiene el token de acceso de Google usando el código de autorización."""
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=current_app.config['GOOGLE_REDIRECT_URI']
    )
    
    flow.fetch_token(code=code)
    credentials = flow.credentials
    
>>>>>>> 646f419
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    } 