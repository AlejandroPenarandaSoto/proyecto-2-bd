from flask import Blueprint, jsonify, request
from src.logica.entidad.habitacion.HabitacionRepo import (
    obtenerHabitaciones,
    obtenerHabitacionPorId,
    insertarHabitacion,
    actualizarHabitacion,
    eliminarHabitacion,
)
from src.logica.entidad.habitacion.Habitacion import Habitacion
from src.Extensions import db

habitacionesBP = Blueprint('habitaciones', __name__, url_prefix='/habitaciones')

def parseBool(value):
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    value = value.lower()
    if value in ['true', '1', 'yes']:
        return True
    elif value in ['false', '0', 'no']:
        return False
    return None

@habitacionesBP.route('/', methods=['GET'])
def getHabitaciones():
    # Obtener filtros desde query params
    tipo = request.args.get('tipo')
    disponible = parseBool(request.args.get('esta_disponible'))
    cama_king = parseBool(request.args.get('cama_king'))
    vista_al_mar = parseBool(request.args.get('vista_al_mar'))
    jacuzzi = parseBool(request.args.get('jacuzzi'))

    try:
        resultados = obtenerHabitaciones(
            dbSession=None,  # Aquí puedes pasar db.session si lo usas dentro
            tipo=tipo,
            disponible=disponible,
            cama_king=cama_king,
            vista_al_mar=vista_al_mar,
            jacuzzi=jacuzzi
        )

        habitaciones = []
        for row in resultados:
            habitacion = dict(row._mapping)  # compatible con SQLAlchemy 1.4+
            habitaciones.append({
                'id_habitacion': habitacion['id_habitacion'],
                'numero': habitacion['numero'],
                'descripcion': habitacion['descripcion'],
                'tipo': habitacion['tipo'],
                'esta_disponible': habitacion['esta_disponible'],
                'cama_king': habitacion['cama_king'],
                'vista_al_mar': habitacion['vista_al_mar'],
                'jacuzzi': habitacion['jacuzzi']
            })

        return jsonify(habitaciones), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@habitacionesBP.route('/<int:idHabitacion>', methods=['GET'])
def getHabitacionPorId(idHabitacion):
    try:
        habitacion = obtenerHabitacionPorId(idHabitacion)
        if habitacion:
            return jsonify(habitacion), 200
        else:
            return jsonify({'error': 'Habitación no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@habitacionesBP.route('/', methods=['POST'])
def createHabitacion():
    data = request.get_json()
    try:
        nuevaHabitacion = Habitacion(
            id_habitacion=None,
            numero=data.get('numero'),
            descripcion=data.get('descripcion'),
            tipo=data.get('tipo'),
            esta_disponible=data.get('esta_disponible', False),
            cama_king=data.get('cama_king', False),
            vista_al_mar=data.get('vista_al_mar', False),
            jacuzzi=data.get('jacuzzi', False)
        )

        insertarHabitacion(nuevaHabitacion)
        return jsonify({'mensaje': 'Habitación creada'}), 201

    except Exception as e:
        return jsonify({'error': f'Error al crear habitación: {str(e)}'}), 500


@habitacionesBP.route('/<int:id>', methods=['PUT'])
def updateHabitacion(id):
    data = request.get_json()
    try:
        habitacionActualizada = Habitacion(
            idHabitacion=id,
            numero=data.get('numero'),
            tipo=data.get('tipo'),
            precio=data.get('precio'),
            estado=data.get('estado')
        )

        actualizarHabitacion(habitacionActualizada)
        return jsonify({'mensaje': 'Habitación actualizada'}), 200

    except Exception as e:
        return jsonify({'error': f'Error al actualizar habitación: {str(e)}'}), 500


@habitacionesBP.route('/<int:idHabitacion>', methods=['DELETE'])
def deleteHabitacion(idHabitacion):
    try:
        eliminarHabitacion(idHabitacion)
        return jsonify({'mensaje': 'Habitación eliminada'}), 200
    except Exception as e:
        if "violates foreign key constraint" in str(e):
            return jsonify({'error': 'No se puede eliminar la habitación porque tiene reservaciones asociadas'}), 409
        return jsonify({'error': f'Error al eliminar habitación: {str(e)}'}), 500