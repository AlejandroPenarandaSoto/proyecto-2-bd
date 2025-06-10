from flask import jsonify
from werkzeug.exceptions import HTTPException
import logging

def RegisterErrorHandlers(app):

    @app.errorhandler(Exception)
    def handle_exception(e):
        # Si es un error HTTP estándar (404, 400, etc)
        if isinstance(e, HTTPException):
            response = {
                "error": {
                    "code": e.code,
                    "name": e.name,
                    "description": e.description,
                }
            }
            app.logger.warning(f"HTTP error: {e.code} {e.name} - {e.description}")
            return jsonify(response), e.code

        # Manejar errores específicos de base de datos (opcional)
        if hasattr(e, 'orig'):  # psycopg2 errors tienen este atributo
            app.logger.error(f"Database error: {e.orig}")
            description = "Error interno en la base de datos."
        else:
            app.logger.error(f"Unhandled exception: {e}")
            description = "Error interno del servidor."

        # No exponer el mensaje real del error en producción
        response = {
            "error": {
                "code": 500,
                "name": "Internal Server Error",
                "description": description,
            }
        }
        return jsonify(response), 500