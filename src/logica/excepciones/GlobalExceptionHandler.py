from flask import jsonify
from werkzeug.exceptions import HTTPException

def RegisterErrorHandlers(app):

    @app.errorhandler(Exception)
    def handle_exception(e):
        # Si es un error HTTP estándar (404, 400, etc)
        if isinstance(e, HTTPException):
            return jsonify({
                "error": {
                    "code": e.code,
                    "name": e.name,
                    "description": e.description,
                }
            }), e.code

        # Para errores no HTTP, responder con 500
        return jsonify({
            "error": {
                "code": 500,
                "name": "Internal Server Error",
                "description": str(e),
            }
        }), 500
