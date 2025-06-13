from flask import Blueprint, jsonify, request
from src.logica.entidad.pago.PagoRepo import (
    obtenerPagos,
    obtenerPagoPorId,
    insertarPago
)
from src.logica.entidad.pago.Pago import Pago

pagosBP = Blueprint('pagos', __name__, url_prefix='/pagos')

@pagosBP.route('/', methods=['GET'])
def getPagos():
    id_usuario = request.args.get('id_usuario', type=int)
    fecha = request.args.get('fecha')
    metodo = request.args.get('metodo')

    try:
        resultados = obtenerPagos(id_usuario=id_usuario, fecha=fecha, metodo=metodo)
        pagos = []

        for row in resultados:
            pago = dict(row._mapping)
            pagos.append(pago)

        return jsonify(pagos), 200
    except Exception as e:
        return jsonify({'error': f'Error al obtener pagos: {str(e)}'}), 500

@pagosBP.route('/<int:idPago>', methods=['GET'])
def getPagoPorId(idPago):
    try:
        pago = obtenerPagoPorId(idPago)
        if pago:
            return jsonify(pago), 200
        else:
            return jsonify({'error': 'Pago no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': f'Error al obtener pago: {str(e)}'}), 500

@pagosBP.route('/', methods=['POST'])
def createPago():
    data = request.get_json()
    try:
        nuevoPago = Pago(
            idPago=None,
            idUsuario=data.get('id_usuario'),
            metodo=data.get('metodo'),
            motivo=data.get('motivo'),
            fecha=data.get('fecha'),
            monto=data.get('monto'),
            idReservacion=data.get('id_reservacion')
        )

        insertarPago(nuevoPago)
        return jsonify({'mensaje': 'Pago registrado correctamente'}), 201
    except Exception as e:
        return jsonify({'error': f'Error al registrar pago: {str(e)}'}), 500