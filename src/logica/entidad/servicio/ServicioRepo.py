from src.Extensions import db
from sqlalchemy import text
from src.logica.entidad.servicio import Servicio

def obtenerServicios(tipo=None, id_pago=None):
    cursorName = 'cursor_servicios'
    callProc = text("""
        CALL sp_obtener_servicios(:ref, :pTipo)
    """)
    fetchCursor = text(f'FETCH ALL FROM "{cursorName}";')
    try:
        with db.engine.begin() as conn:
            conn.execute(callProc, {
                'ref': cursorName,
                'pTipo': tipo
            })
            result = conn.execute(fetchCursor)
            return result.fetchall()
    except Exception as e:
        raise e

def obtenerServicioPorId(idServicio):
    cursorName = 'cursor_servicios'
    callProc = text("""CALL sp_servicio_por_id(:p_id_servicio, :ref)""")
    fetchCursor = text(f'FETCH ALL FROM "{cursorName}";')
    try:
        with db.engine.begin() as conn:
            conn.execute(callProc, {'p_id_servicio': idServicio, 'ref': cursorName})
            result = conn.execute(fetchCursor)
            row = result.fetchone()
            return dict(row._mapping) if row else None
    except Exception as e:
        print(f"Error en obtenerServicioPorId: {e}")
        raise e

def insertarServicio(servicio: Servicio):
    sp_call = text("""
        CALL sp_insertar_servicio(
            :p_id_hotel,
            :p_tipo,
            :p_monto_promocion,
            :p_reembolso,
            :p_motivo_cargo,
            :p_cargo_extra,
            :p_monto_base,
            :p_id_pago
        )
    """)
    try:
        with db.engine.begin() as conn:
            conn.execute(sp_call, {
                'p_id_hotel': servicio.idHotel,
                'p_tipo': servicio.tipo,
                'p_monto_promocion': servicio.montoPromocion,
                'p_reembolso': servicio.reembolso,
                'p_motivo_cargo': servicio.motivoCargo,
                'p_cargo_extra': servicio.cargoExtra,
                'p_monto_base': servicio.montoBase,
                'p_id_pago': servicio.idPago
            })
    except Exception as e:
        print(f"Error insertando servicio: {e}")
        raise

def actualizarServicio(servicio: Servicio):
    sp_call = text("""
        CALL sp_actualizar_servicio(
            :p_id_servicio,
            :p_tipo,
            :p_monto_promocion,
            :p_reembolso,
            :p_motivo_cargo,
            :p_cargo_extra,
            :p_monto_base
        )
    """)
    try:
        with db.engine.begin() as conn:
            conn.execute(sp_call, {
                'p_id_servicio': servicio.idServicio,
                'p_tipo': servicio.tipo,
                'p_monto_promocion': servicio.montoPromocion,
                'p_reembolso': servicio.reembolso,
                'p_motivo_cargo': servicio.motivoCargo,
                'p_cargo_extra': servicio.cargoExtra,
                'p_monto_base': servicio.montoBase
            })
    except Exception as e:
        print(f"Error actualizando servicio: {e}")
        raise

def eliminarServicio(idServicio):
    sp_call = text("CALL sp_eliminar_servicio(:p_id_servicio)")
    try:
        with db.engine.begin() as conn:
            conn.execute(sp_call, {"p_id_servicio": idServicio})
    except Exception as e:
        print(f"Error eliminando servicio: {e}")
        raise
