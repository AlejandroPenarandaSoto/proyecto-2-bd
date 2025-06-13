from flask import Blueprint, jsonify, request
from src.logica.entidad.usuario.UsuarioRepo import (
    obtenerUsuarios,
    obtenerUsuarioPorId,
    insertarUsuario,
    actualizarUsuario,
    eliminarUsuario,
)
from src.logica.entidad.usuario.Usuario import Usuario
from sqlalchemy import text
from src.Extensions import db
import re

clientesBP = Blueprint('clientes', __name__, url_prefix='/clientes')

@clientesBP.route('/', methods=['GET'])
def obtenerClientes():
    pNombre = request.args.get('nombre')
    pNacionalidad = request.args.get('nacionalidad')
    pCorreo = request.args.get('correo')

    try:
        usuarios = obtenerUsuarios(db.session, pNombre, pNacionalidad, pCorreo)
        clientes = []

        for row in usuarios:
            cliente = dict(row._mapping)  # más robusto para SQLAlchemy 1.4+
            clientes.append({
                'nombre': cliente['nombre'],
                'nacionalidad': cliente['nacionalidad'],
                'telefono': cliente['telefono'],
                'correo': cliente['correo'],
            })

        return jsonify(clientes)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@clientesBP.route('/<int:idUsuario>', methods=['GET'])
def getClienteId(idUsuario):
    try:
        usuario = obtenerUsuarioPorId(idUsuario)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'error': 'Cliente no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def validarEmail(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email) is not None

@clientesBP.route('/', methods=['POST'])
def createCliente():
    data = request.get_json()
    try:
        email = data.get('correo')

        if not email or not validarEmail(email):
            return jsonify({'error': 'Correo electrónico inválido'}), 400

        nuevoUsuario = Usuario(
            idUsuario=None,
            nacionalidad=data.get('nacionalidad'),
            nombre=data.get('nombre'),
            docIdentidad=data.get('docIdentidad'),
            telefono=data.get('telefono'),
            correo=email,
            contrasena=data.get('contrasena')
        )

        insertarUsuario(nuevoUsuario)
        return jsonify({'mensaje': 'Cliente creado'}), 201

    except Exception as e:
        return jsonify({'error': f'Error al crear cliente: {str(e)}'}), 500

@clientesBP.route('/<int:id>', methods=['PUT'])
def updateCliente(id):
    data = request.get_json()
    try:
        email = data.get('correo')

        if not email or not validarEmail(email):
            return jsonify({'error': 'Correo electrónico inválido'}), 400

        usuarioActualizado = Usuario(
            idUsuario=id,
            nacionalidad=data.get('nacionalidad'),
            nombre=data.get('nombre'),
            docIdentidad=data.get('docIdentidad'),
            telefono=data.get('telefono'),
            correo=email,
            contrasena=data.get('contrasena')
        )

        actualizarUsuario(usuarioActualizado)
        return jsonify({'mensaje': 'Cliente actualizado'}), 200

    except Exception as e:
        return jsonify({'error': f'Error al actualizar cliente: {str(e)}'}), 500


@clientesBP.route('/clientes/<int:idUsuario>', methods=['DELETE'])
def deleteCliente(idUsuario):
    eliminarUsuario(idUsuario)
    return jsonify({'mensaje': 'Cliente eliminado'})
