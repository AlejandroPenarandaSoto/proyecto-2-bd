from flask import Blueprint, jsonify, request
from src.logica.entidad.usuario.UsuarioRepo import (
    obtenerUsuarios,
    obtenerUsuarioPorId,
    insertarUsuario,
    actualizarUsuario,
    eliminarUsuario,
)
from src.logica.entidad.usuario import Usuario
from sqlalchemy import text
from src.Extensions import db

clientesBP = Blueprint('clientes', __name__, url_prefix='/clientes')

@clientesBP.route('/', methods=['GET'])
def obtenerClientes():
    pNombre = request.args.get('nombre')
    pNacionalidad = request.args.get('nacionalidad')
    pCorreo = request.args.get('correo')

    cursorName = 'cursor_usuarios'
    callProc = text("""
        CALL sp_obtener_usuarios(:ref, :p_nombre, :p_nacionalidad, :p_correo)
    """)

    trans = None
    try:
        with db.engine.connect() as conn:
            trans = conn.begin()

            conn.execute(callProc, {
                'ref': cursorName,
                'p_nombre': pNombre,
                'p_nacionalidad': pNacionalidad,
                'p_correo': pCorreo
            })

            fetchCursor = text(f'FETCH ALL FROM "{cursorName}";')
            result = conn.execute(fetchCursor)

            trans.commit()

        clientes = []
        keys = result.keys()
        for row in result:
            cliente = dict(zip(keys, row))
            clientes.append({
                'nombre': cliente['nombre'],
                'nacionalidad': cliente['nacionalidad'],
                'telefono': cliente['telefono'],
                'correo': cliente['correo'],
            })

        return jsonify(clientes)

    except Exception:
        if trans is not None:
            trans.rollback()
        raise

@clientesBP.route('/clientes/<int:idUsuario>', methods=['GET'])
def getClienteId(idUsuario):
    usuario = obtenerUsuarioPorId(idUsuario)
    if usuario:
        return jsonify(usuario.to_dict())
    return jsonify({'error': 'Cliente no encontrado'}), 404


@clientesBP.route('/clientes', methods=['POST'])
def createCliente():
    data = request.get_json()
    nuevoUsuario = Usuario(
        idUsuario=None,
        nacionalidad=data.get('nacionalidad'),
        nombre=data.get('nombre'),
        docIdentidad=data.get('docIdentidad'),
        telefono=data.get('telefono'),
        correo=data.get('correo'),
        contrasena=data.get('contrasena')
    )
    insertarUsuario(nuevoUsuario)
    return jsonify({'mensaje': 'Cliente creado'}), 201


@clientesBP.route('/clientes/<int:idUsuario>', methods=['PUT'])
def updateCliente(idUsuario):
    data = request.get_json()
    usuario = Usuario(
        idUsuario=idUsuario,
        nacionalidad=data.get('nacionalidad'),
        nombre=data.get('nombre'),
        docIdentidad=data.get('docIdentidad'),
        telefono=data.get('telefono'),
        correo=data.get('correo'),
        contrasena=data.get('contrasena')
    )
    actualizarUsuario(usuario)
    return jsonify({'mensaje': 'Cliente actualizado'})


@clientesBP.route('/clientes/<int:idUsuario>', methods=['DELETE'])
def deleteCliente(idUsuario):
    eliminarUsuario(idUsuario)
    return jsonify({'mensaje': 'Cliente eliminado'})
