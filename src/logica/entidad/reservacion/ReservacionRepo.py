from src.Extensions import db
from sqlalchemy import text
from src.logica.entidad.reservacion import Reservacion

from src.Extensions import db
from sqlalchemy import text
from datetime import datetime

def obtenerReservaciones(estado=None, id_usuario=None):
    cursorName = 'cursor_reservaciones'
    callProc = text("""
        CALL sp_obtener_reservaciones(:ref, :pEstado, :pIdUsuario)
    """)
    fetchCursor = text(f'FETCH ALL FROM "{cursorName}";')
    try:
        with db.engine.begin() as conn:
            conn.execute(callProc, {
                'ref': cursorName,
                'pEstado': estado,
                'pIdUsuario': id_usuario
            })
            result = conn.execute(fetchCursor)
            return result.fetchall()
    except Exception as e:
        raise e

def obtenerReservacionPorId(idReservacion):
    cursorName = 'cursor_reservaciones'
    callProc = text("CALL sp_reservacion_por_id(:p_id_reservacion, :ref)")
    fetchCursor = text(f'FETCH ALL FROM "{cursorName}";')
    try:
        with db.engine.begin() as conn:
            conn.execute(callProc, {'p_id_reservacion': idReservacion, 'ref': cursorName})
            result = conn.execute(fetchCursor)
            row = result.fetchone()
            return dict(row._mapping) if row else None
    except Exception as e:
        print(f"Error en obtenerReservacionPorId: {e}")
        raise e

def insertarReservacion(reservacion: Reservacion):
    sp_call = text("""
        CALL sp_insertar_reservacion(
            :p_id_hotel,
            :p_id_usuario,
            :p_ids_habitacion,
            :p_solicitudes,
            :p_num_huespedes,
            :p_num_noches,
            :p_fecha_llegada,
            :p_fecha_salida,
            :p_estado,
            :p_total_apagar
        )
    """)
    try:
        with db.engine.begin() as conn:
            conn.execute(sp_call, {
                'p_id_hotel': reservacion.idHotel,
                'p_id_usuario': reservacion.idUsuario,
                'p_ids_habitacion': reservacion.idsHabitacion,
                'p_solicitudes': reservacion.solicitudes,
                'p_num_huespedes': reservacion.numHuespedes,
                'p_num_noches': reservacion.numNoches,
                'p_fecha_llegada': reservacion.fechaLlegada,
                'p_fecha_salida': reservacion.fechaSalida,
                'p_estado': reservacion.estado,
                'p_total_apagar': reservacion.totalApagar
            })
    except Exception as e:
        print(f"Error insertando reservacion: {e}")
        raise

def actualizarReservacion(reservacion: Reservacion):
    sp_call = text("""
        CALL sp_actualizar_reservacion(
            :p_id_reservacion,
            :p_solicitudes,
            :p_num_huespedes,
            :p_num_noches,
            :p_fecha_llegada,
            :p_fecha_salida,
            :p_monto_apagar
        )
    """)
    try:
        with db.engine.begin() as conn:
            conn.execute(sp_call, {
                'p_id_reservacion': reservacion.idReservacion,
                'p_solicitudes': reservacion.solicitudes,
                'p_num_huespedes': reservacion.numHuespedes,
                'p_num_noches': reservacion.numNoches,
                'p_fecha_llegada': reservacion.fechaLlegada,
                'p_fecha_salida': reservacion.fechaSalida,
                'p_monto_apagar': reservacion.totalApagar
            })
    except Exception as e:
        print(f"Error actualizando reservacion: {e}")
        raise

def eliminarReservacion(idReservacion):
    sp_call = text("CALL sp_eliminar_reservacion(:p_id_reservacion)")
    try:
        with db.engine.begin() as conn:
            conn.execute(sp_call, {"p_id_reservacion": idReservacion})
    except Exception as e:
        print(f"Error eliminando reservacion: {e}")
        raise
