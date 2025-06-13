from src.Extensions import db
from sqlalchemy import text
from src.logica.entidad.usuario import Usuario

def obtenerUsuarios(dbSession, nombre=None, nacionalidad=None, correo=None):
    cursorName = 'cursor_usuarios'
    callProc = text("""
        CALL sp_obtener_usuarios(:ref, :pNombre, :pNacionalidad, :pCorreo)
    """)
    fetchCursor = text(f'FETCH ALL FROM "{cursorName}";')

    try:
        with db.engine.begin() as conn:
            conn.execute(callProc, {
                'ref': cursorName,
                'pNombre': nombre,
                'pNacionalidad': nacionalidad,
                'pCorreo': correo
            })
            result = conn.execute(fetchCursor)
            return result.fetchall()
    except Exception as e:
        raise e

def obtenerUsuarioPorId(idUsuario):
    cursorName = 'cursor_usuarios'
    callProc = text("""CALL sp_usuario_por_id(:p_id_usuario, :ref)""")
    fetchCursor = text(f'FETCH ALL FROM "{cursorName}";')
    try:
        with db.engine.begin() as conn:
            conn.execute(callProc, {'p_id_usuario': idUsuario, 'ref': cursorName})
            result = conn.execute(fetchCursor)
            row = result.fetchone()
            return dict(row._mapping) if row else None
    except Exception as e:
        print(f"Error en obtenerUsuarioPorId: {e}")
        raise e


def insertarUsuario(usuario: Usuario):
    db.session.execute(
        "CALL insertar_usuario(:nacionalidad, :nombre, :docIdentidad, :telefono, :correo, :contrasena)",
        {
            "nacionalidad": usuario.nacionalidad,
            "nombre": usuario.nombre,
            "docIdentidad": usuario.docIdentidad,
            "telefono": usuario.telefono,
            "correo": usuario.correo,
            "contrasena": usuario.contrasena,
        },
    )
    db.session.commit()


def actualizarUsuario(usuario: Usuario):
    db.session.execute(
        "CALL sp_actualizar_usuario(:idUsuario, :nacionalidad, :nombre, :docIdentidad, :telefono, :correo, :contrasena)",
        {
            "idUsuario": usuario.idUsuario,
            "nacionalidad": usuario.nacionalidad,
            "nombre": usuario.nombre,
            "docIdentidad": usuario.docIdentidad,
            "telefono": usuario.telefono,
            "correo": usuario.correo,
            "contrasena": usuario.contrasena,
        },
    )
    db.session.commit()


def eliminarUsuario(idUsuario):
    db.session.execute("CALL sp_eliminar_usuario(:idUsuario)", {"idUsuario": idUsuario})
    db.session.commit()
