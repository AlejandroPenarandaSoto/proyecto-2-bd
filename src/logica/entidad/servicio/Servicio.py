from typing import Optional

class Servicio:
    def __init__(self,
                 idServicio: int,
                 idHotel: int,
                 tipo: str,
                 montoPromocion: float,
                 reembolso: float,
                 motivoCargo: str,
                 cargoExtra: float,
                 montoBase: float,
                 idPago: Optional[int] = None
                 ):
        self.idServicio = idServicio
        self.idHotel = idHotel
        self.tipo = tipo
        self.montoPromocion = montoPromocion
        self.reembolso = reembolso
        self.motivoCargo = motivoCargo
        self.cargoExtra = cargoExtra
        self.montoBase = montoBase
        self.idPago = idPago

    def to_dict(self):
        return {
            "idServicio": self.idServicio,
            "idHotel": self.idHotel,
            "tipo": self.tipo,
            "montoPromocion": self.montoPromocion,
            "reembolso": self.reembolso,
            "motivoCargo": self.motivoCargo,
            "cargoExtra": self.cargoExtra,
            "montoBase": self.montoBase,
            "idPago": self.idPago
        }
