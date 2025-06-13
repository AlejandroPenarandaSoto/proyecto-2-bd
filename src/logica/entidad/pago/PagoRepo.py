from src.Extensions import db
from sqlalchemy import text
from datetime import datetime
from decimal import Decimal
from src.logica.entidad.pago import Pago  # asumiendo ruta

def obtenerPagos(id_usuario=None, fecha=None, metodo=None):
    cursorName = 'cursor_pagos'
    callProc = text("""
        CALL sp_obtener_pagos(:ref, :p_id_usuario, :p_fecha, :p_metodo)
    """)
    fetchCursor = text(f'FETCH ALL FROM "{cursorName}";')
    try:
        with db.engine.begin() as conn:
            conn.execute(callProc, {
                'ref': cursorName,
                'p_id_usuario': id_usuario,
                'p_fecha': fecha,
                'p_metodo': metodo
            })
            result = conn.execute(fetchCursor)
            return result.fetchall()
    except Exception as e:
        print(f"Error obteniendo pagos: {e}")
        raise

def obtenerPagoPorId(id_pago):
    cursorName = 'cursor_pagos'
    callProc = text("CALL sp_pago_por_id(:p_id_pago, :ref)")
    fetchCursor = text(f'FETCH ALL FROM "{cursorName}";')
    try:
        with db.engine.begin() as conn:
            conn.execute(callProc, {'p_id_pago': id_pago, 'ref': cursorName})
            result = conn.execute(fetchCursor)
            row = result.fetchone()
            return dict(row._mapping) if row else None
    except Exception as e:
        print(f"Error obteniendo pago por ID: {e}")
        raise

def insertarPago(pago: Pago):
    sp_call = text("""
        CALL sp_insertar_pago(
            :p_id_usuario,
            :p_metodo,
            :p_motivo,
            :p_fecha,
            :p_monto,
            :p_id_reservacion
        )
    """)
    try:
        with db.engine.begin() as conn:
            conn.execute(sp_call, {
                'p_id_usuario': pago.idUsuario,
                'p_metodo': pago.metodo,
                'p_motivo': pago.motivo,
                'p_fecha': pago.fecha,
                'p_monto': pago.monto,
                'p_id_reservacion': pago.idReservacion
            })
    except Exception as e:
        print(f"Error insertando pago: {e}")
        raise