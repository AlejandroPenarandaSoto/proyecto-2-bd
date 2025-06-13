class Habitacion:
    def __init__(self, id_habitacion, numero, descripcion, tipo,
                 esta_disponible=False, cama_king=False, vista_al_mar=False, jacuzzi=False):
        self.id_habitacion = id_habitacion
        self.numero = numero
        self.descripcion = descripcion
        self.tipo = tipo
        self.esta_disponible = esta_disponible
        self.cama_king = cama_king
        self.vista_al_mar = vista_al_mar
        self.jacuzzi = jacuzzi

    def to_dict(self):
        return {
            "id_habitacion": self.id_habitacion,
            "numero": self.numero,
            "descripcion": self.descripcion,
            "tipo": self.tipo,
            "esta_disponible": self.esta_disponible,
            "cama_king": self.cama_king,
            "vista_al_mar": self.vista_al_mar,
            "jacuzzi": self.jacuzzi
        }
