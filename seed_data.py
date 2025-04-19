from app import create_app
from app.database import db
from app.models import User, Advisor

app = create_app()

with app.app_context():
    # Crear usuario
    user = User(
        username='gonzalo',
        email='gonzalo@pidomas.com'
    )
    db.session.add(user)
    
    # Crear asesor
    advisor = Advisor(
        name='Contacto',
        email='contacto@pidomas.com'
    )
    db.session.add(advisor)
    
    # Guardar cambios
    db.session.commit()
    print("Datos sembrados exitosamente!") 