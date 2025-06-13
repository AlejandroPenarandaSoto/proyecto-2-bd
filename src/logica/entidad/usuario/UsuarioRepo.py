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


def insertarUsuario(usuario):
    sp_call = text("""
        CALL sp_insertar_usuario(:p_nacionalidad, :p_nombre, :p_doc_identidad, :p_telefono, :p_correo, :p_contrasena)
    """)
    try:
        with db.engine.begin() as conn:
            conn.execute(sp_call, {
                'p_nacionalidad': usuario.nacionalidad,
                'p_nombre': usuario.nombre,
                'p_doc_identidad': usuario.docIdentidad,
                'p_telefono': usuario.telefono,
                'p_correo': usuario.correo,
                'p_contrasena': usuario.contrasena,
            })
    except Exception as e:
        print(f"Error insertando usuario: {e}")
        raise


def actualizarUsuario(usuario: Usuario):
    sp_call = text("""
        CALL sp_actualizar_usuario(:p_id_usuario, :p_nacionalidad, :p_nombre, :p_doc_identidad, :p_telefono, :p_correo, :p_contrasena)
    """)
    try:
        with db.engine.begin() as conn:  # begin para commit automático
            conn.execute(sp_call, {
                'p_id_usuario': usuario.idUsuario,
                'p_nacionalidad': usuario.nacionalidad,
                'p_nombre': usuario.nombre,
                'p_doc_identidad': usuario.docIdentidad,
                'p_telefono': usuario.telefono,
                'p_correo': usuario.correo,
                'p_contrasena': usuario.contrasena,
            })
    except Exception as e:
        print(f"Error actualizando usuario: {e}")
        raise

def eliminarUsuario(idUsuario):
    sp_call = text("CALL sp_eliminar_usuario(:p_id_usuario)")
    try:
        with db.engine.begin() as conn:  # maneja automáticamente el commit
            conn.execute(sp_call, {"p_id_usuario": idUsuario})
    except Exception as e:
        print(f"Error eliminando usuario: {e}")
        raise
