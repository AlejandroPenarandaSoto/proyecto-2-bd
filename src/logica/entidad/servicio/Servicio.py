from typing import Optional

class Servicio:
    def __init__(self,
                 idServicio: Optional[int],
                 idHotel: Optional[int] = None,
                 tipo: str = '',
                 montoPromocion: float = 0.0,
                 reembolso: float = 0.0,
                 motivoCargo: str = '',
                 cargoExtra: float = 0.0,
                 montoBase: float = 0.0,
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