from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from .Extensions import db
from .logica.excepciones.GlobalExceptionHandler import RegisterErrorHandlers
from .rest.usuario.UsuarioController import clientesBP
from .rest.habitacion.HabitacionController import habitacionesBP
from .rest.reservacion.ReservcacionController import reservacionesBP
from .rest.pago.PagoController import pagosBP

def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)


    app.register_blueprint(clientesBP)
    app.register_blueprint(habitacionesBP)
    app.register_blueprint(reservacionesBP)
    app.register_blueprint(pagosBP)

    RegisterErrorHandlers(app)

    return app
