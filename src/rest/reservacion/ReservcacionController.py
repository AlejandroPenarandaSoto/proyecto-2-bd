from flask import Blueprint, jsonify, request
from src.logica.entidad.reservacion.ReservacionRepo import (
    obtenerReservaciones,
    obtenerReservacionPorId,
    insertarReservacion,
    actualizarReservacion,
    eliminarReservacion
)
from src.logica.entidad.reservacion.Reservacion import Reservacion

reservacionesBP = Blueprint('reservaciones', __name__, url_prefix='/reservaciones')

@reservacionesBP.route('/', methods=['GET'])
def getReservaciones():
    estado = request.args.get('estado')
    id_usuario = request.args.get('id_usuario', type=int)

    try:
        resultados = obtenerReservaciones(estado=estado, id_usuario=id_usuario)
        reservaciones = []

        for row in resultados:
            reservacion = dict(row._mapping)
            reservaciones.append(reservacion)

        return jsonify(reservaciones), 200
    except Exception as e:
        return jsonify({'error': f'Error al obtener reservaciones: {str(e)}'}), 500

@reservacionesBP.route('/<int:idReservacion>', methods=['GET'])
def getReservacionPorId(idReservacion):
    try:
        reservacion = obtenerReservacionPorId(idReservacion)
        if reservacion:
            return jsonify(reservacion), 200
        else:
            return jsonify({'error': 'Reservación no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': f'Error al obtener reservación: {str(e)}'}), 500

@reservacionesBP.route('/', methods=['POST'])
def createReservacion():
    data = request.get_json()
    try:
        nuevaReservacion = Reservacion(
            idReservacion=None,
            idHotel=data.get('id_hotel'),
            idUsuario=data.get('id_usuario'),
            idsHabitacion=data.get('ids_habitacion'),  # Lista o string, según cómo lo esperes
            solicitudes=data.get('solicitudes'),
            numHuespedes=data.get('num_huespedes'),
            numNoches=data.get('num_noches'),
            fechaLlegada=data.get('fecha_llegada'),
            fechaSalida=data.get('fecha_salida'),
            estado=data.get('estado'),
            totalApagar=data.get('total_apagar')
        )

        insertarReservacion(nuevaReservacion)
        return jsonify({'mensaje': 'Reservación creada correctamente'}), 201
    except Exception as e:
        return jsonify({'error': f'Error al crear reservación: {str(e)}'}), 500

@reservacionesBP.route('/<int:id>', methods=['PUT'])
def updateReservacion(id):
    data = request.get_json()
    try:
        reservacionActualizada = Reservacion(
            idReservacion=id,
            solicitudes=data.get('solicitudes'),
            numHuespedes=data.get('num_huespedes'),
            numNoches=data.get('num_noches'),
            fechaLlegada=data.get('fecha_llegada'),
            fechaSalida=data.get('fecha_salida'),
            totalApagar=data.get('total_apagar')
        )

        actualizarReservacion(reservacionActualizada)
        return jsonify({'mensaje': 'Reservación actualizada correctamente'}), 200
    except Exception as e:
        return jsonify({'error': f'Error al actualizar reservación: {str(e)}'}), 500

@reservacionesBP.route('/<int:idReservacion>', methods=['DELETE'])
def deleteReservacion(idReservacion):
    try:
        eliminarReservacion(idReservacion)
        return jsonify({'mensaje': 'Reservación eliminada correctamente'}), 200
    except Exception as e:
        return jsonify({'error': f'Error al eliminar reservación: {str(e)}'}), 500
