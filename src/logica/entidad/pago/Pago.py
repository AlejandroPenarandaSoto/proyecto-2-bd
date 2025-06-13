from datetime import date
from decimal import Decimal

class Pago:
    def __init__(self,
                 idPago: int,
                 idUsuario: int,
                 metodo: str,
                 motivo: str,
                 fecha: date,
                 monto: Decimal,
                 idReservacion: int):
        self.idPago = idPago
        self.idUsuario = idUsuario
        self.metodo = metodo
        self.motivo = motivo
        self.fecha = fecha
        self.monto = monto
        self.idReservacion = idReservacion

    def to_dict(self):
        return {
            "idPago": self.idPago,
            "idUsuario": self.idUsuario,
            "metodo": self.metodo,
            "motivo": self.motivo,
            "fecha": self.fecha.isoformat(),
            "monto": float(self.monto),
            "idReservacion": self.idReservacion
        }