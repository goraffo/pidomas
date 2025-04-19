from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from .database import db
import os

def create_app():
    app = Flask(__name__)
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Configuración básica
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Inicializar migraciones
    migrate = Migrate(app, db)
    
    # Importar modelos
    from . import models
    
    # Registrar blueprints
    from .routes.calendar import calendar_bp
    app.register_blueprint(calendar_bp)
    
    return app 