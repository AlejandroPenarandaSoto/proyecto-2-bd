from src.Extensions import db
from sqlalchemy import text
from src.logica.entidad.usuario import Usuario

def obtenerUsuarios(dbSession, nombre=None, nacionalidad=None, correo=None):
    cursorName = 'cursorUsuarios'
    callProc = text("""
        CALL sp_obtener_usuarios(:ref, :pNombre, :pNacionalidad, :pCorreo)
    """)
    fetchCursor = text(f'FETCH ALL FROM "{cursorName}";')

    try:
        with dbSession.connection() as conn:
            trans = conn.begin()
            conn.execute(callProc, {
                'ref': cursorName,
                'pNombre': nombre,
                'pNacionalidad': nacionalidad,
                'pCorreo': correo
            })
            result = conn.execute(fetchCursor)
            trans.commit()

            return result.fetchall()

    except Exception:
        trans.rollback()
        raise



def obtenerUsuarioPorId(idUsuario):
    result = db.session.execute("CALL usuario_por_id(:idUsuario)", {"idUsuario": idUsuario})
    row = result.fetchone()
    return Usuario(**dict(row)) if row else None


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
