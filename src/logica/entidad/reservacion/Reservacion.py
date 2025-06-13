from datetime import datetime
from decimal import Decimal
from typing import Optional, List

class Reservacion:
    def __init__(self,
                 idReservacion: Optional[int] = None,
                 idHotel: Optional[int] = None,
                 idUsuario: Optional[int] = None,
                 solicitudes: Optional[str] = None,
                 numHuespedes: Optional[int] = None,
                 numNoches: Optional[int] = None,
                 fechaLlegada: Optional[datetime] = None,
                 fechaSalida: Optional[datetime] = None,
                 estado: Optional[str] = None,
                 totalApagar: Optional[Decimal] = None,
                 idsHabitacion: Optional[List[int]] = None
                 ):
        self.idReservacion = idReservacion
        self.idHotel = idHotel
        self.idUsuario = idUsuario
        self.solicitudes = solicitudes
        self.numHuespedes = numHuespedes
        self.numNoches = numNoches
        self.fechaLlegada = fechaLlegada
        self.fechaSalida = fechaSalida
        self.estado = estado
        self.totalApagar = totalApagar
        self.idsHabitacion = idsHabitacion or []

    def to_dict(self, include_ids_habitacion: bool = False):
        data = {
            "idReservacion": self.idReservacion,
            "idHotel": self.idHotel,
            "idUsuario": self.idUsuario,
            "solicitudes": self.solicitudes,
            "numHuespedes": self.numHuespedes,
            "numNoches": self.numNoches,
            "fechaLlegada": self.fechaLlegada.isoformat() if self.fechaLlegada else None,
            "fechaSalida": self.fechaSalida.isoformat() if self.fechaSalida else None,
            "estado": self.estado,
            "totalApagar": float(self.totalApagar) if self.totalApagar is not None else None
        }
        if include_ids_habitacion:
            data["idsHabitacion"] = self.idsHabitacion
        return data