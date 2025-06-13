from src.Extensions import db
from sqlalchemy import text
from src.logica.entidad.habitacion import Habitacion

def obtenerHabitaciones(dbSession, tipo=None, disponible=None, cama_king=None, vista_al_mar=None, jacuzzi=None):
    cursorName = 'cursor_habitaciones'
    callProc = text("""
        CALL sp_obtener_habitaciones(:ref, :pTipo, :pDisponible, :pCamaKing, :pVistaAlMar, :pJacuzzi)
    """)
    fetchCursor = text(f'FETCH ALL FROM "{cursorName}";')
    try:
        with db.engine.begin() as conn:
            conn.execute(callProc, {
                'ref': cursorName,
                'pTipo': tipo,
                'pDisponible': disponible,
                'pCamaKing': cama_king,
                'pVistaAlMar': vista_al_mar,
                'pJacuzzi': jacuzzi
            })
            result = conn.execute(fetchCursor)
            return result.fetchall()
    except Exception as e:
        raise e


def obtenerHabitacionPorId(id_habitacion):
    cursorName = 'cursor_habitaciones'
    callProc = text("""CALL sp_habitacion_por_id(:p_id_habitacion, :ref)""")
    fetchCursor = text(f'FETCH ALL FROM "{cursorName}";')
    try:
        with db.engine.begin() as conn:
            conn.execute(callProc, {'p_id_habitacion': id_habitacion, 'ref': cursorName})
            result = conn.execute(fetchCursor)
            row = result.fetchone()
            return dict(row._mapping) if row else None
    except Exception as e:
        print(f"Error en obtenerHabitacionPorId: {e}")
        raise e


def insertarHabitacion(habitacion: Habitacion):
    sp_call = text("""
        CALL sp_insertar_habitacion(:p_numero, :p_descripcion, :p_tipo, :p_esta_disponible, :p_cama_king, :p_vista_al_mar, :p_jacuzzi)
    """)
    try:
        with db.engine.begin() as conn:
            conn.execute(sp_call, {
                'p_numero': habitacion.numero,
                'p_descripcion': habitacion.descripcion,
                'p_tipo': habitacion.tipo,
                'p_esta_disponible': habitacion.esta_disponible,
                'p_cama_king': habitacion.cama_king,
                'p_vista_al_mar': habitacion.vista_al_mar,
                'p_jacuzzi': habitacion.jacuzzi
            })
    except Exception as e:
        print(f"Error insertando habitacion: {e}")
        raise


def actualizarHabitacion(habitacion: Habitacion):
    sp_call = text("""
        CALL sp_actualizar_habitacion(:p_id_habitacion, :p_numero, :p_descripcion, :p_tipo, :p_esta_disponible, :p_cama_king, :p_vista_al_mar, :p_jacuzzi)
    """)
    try:
        with db.engine.begin() as conn:
            conn.execute(sp_call, {
                'p_id_habitacion': habitacion.id_habitacion,
                'p_numero': habitacion.numero,
                'p_descripcion': habitacion.descripcion,
                'p_tipo': habitacion.tipo,
                'p_esta_disponible': habitacion.esta_disponible,
                'p_cama_king': habitacion.cama_king,
                'p_vista_al_mar': habitacion.vista_al_mar,
                'p_jacuzzi': habitacion.jacuzzi
            })
    except Exception as e:
        print(f"Error actualizando habitacion: {e}")
        raise


def eliminarHabitacion(id_habitacion):
    sp_call = text("CALL sp_eliminar_habitacion(:p_id_habitacion)")
    try:
        with db.engine.begin() as conn:
            conn.execute(sp_call, {"p_id_habitacion": id_habitacion})
    except Exception as e:
        print(f"Error eliminando habitacion: {e}")
        raise
