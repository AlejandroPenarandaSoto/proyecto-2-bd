from flask import Blueprint, jsonify, request
from src.logica.entidad.servicio.ServicioRepo import (
    obtenerServicios,
    obtenerServicioPorId,
    insertarServicio,
    actualizarServicio,
    eliminarServicio,
)
from src.logica.entidad.servicio.Servicio import Servicio
from src.Extensions import db

serviciosBP = Blueprint('servicios', __name__, url_prefix='/servicios')

@serviciosBP.route('/', methods=['GET'])
def getServicios():
    tipo = request.args.get('tipo')
    id_pago = request.args.get('id_pago', type=int)
    try:
        resultados = obtenerServicios(
            tipo=tipo,
            id_pago=id_pago
        )
        servicios = []
        for row in resultados:
            servicio = dict(row._mapping)
            servicios.append(servicio)
        return jsonify(servicios), 200
    except Exception as e:
        return jsonify({'error': f'Error al obtener servicios: {str(e)}'}), 500

@serviciosBP.route('/<int:idServicio>', methods=['GET'])
def getServicioPorId(idServicio):
    try:
        servicio = obtenerServicioPorId(idServicio)
        if servicio:
            return jsonify(servicio), 200
        else:
            return jsonify({'error': 'Servicio no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@serviciosBP.route('/', methods=['POST'])
def createServicio():
    data = request.get_json()
    id_hotel = data.get('id_hotel')
    if id_hotel is None:
        return jsonify({'error': 'id_hotel es obligatorio'}), 400
    try:
        nuevoServicio = Servicio(
            idServicio=None,
            idHotel=id_hotel,
            idPago=data.get('id_pago'),
            tipo=data.get('tipo'),
            montoPromocion=data.get('monto_promocion'),
            reembolso=data.get('reembolso'),
            motivoCargo=data.get('motivo_cargo'),
            cargoExtra=data.get('cargo_extra'),
            montoBase=data.get('monto_base')
        )
        insertarServicio(nuevoServicio)
        return jsonify({'mensaje': 'Servicio creado'}), 201
    except Exception as e:
        return jsonify({'error': f'Error al crear servicio: {str(e)}'}), 500

@serviciosBP.route('/<int:id>', methods=['PUT'])
def updateServicio(id):
    data = request.get_json()
    try:
        servicioActualizado = Servicio(
            idServicio=id,
            tipo=data.get('tipo'),
            montoPromocion=data.get('monto_promocion'),
            reembolso=data.get('reembolso'),
            motivoCargo=data.get('motivo_cargo'),
            cargoExtra=data.get('cargo_extra'),
            montoBase=data.get('monto_base')
        )

        actualizarServicio(servicioActualizado)
        return jsonify({'mensaje': 'Servicio actualizado'}), 200
    except Exception as e:
        return jsonify({'error': f'Error al actualizar servicio: {str(e)}'}), 500

@serviciosBP.route('/<int:idServicio>', methods=['DELETE'])
def deleteServicio(idServicio):
    try:
        eliminarServicio(idServicio)
        return jsonify({'mensaje': 'Servicio eliminado'}), 200
    except Exception as e:
        if "violates foreign key constraint" in str(e):
            return jsonify({'error': 'No se puede eliminar el servicio porque tiene dependencias asociadas'}), 409
        return jsonify({'error': f'Error al eliminar servicio: {str(e)}'}), 500
