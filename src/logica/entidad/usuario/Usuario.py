class Usuario:
    def __init__(self, idUsuario, nacionalidad, nombre, docIdentidad, telefono, correo, contrasena):
        self.idUsuario = idUsuario
        self.nacionalidad = nacionalidad
        self.nombre = nombre
        self.docIdentidad = docIdentidad
        self.telefono = telefono
        self.correo = correo
        self.contrasena = contrasena

    def to_dict(self):
        return {
            "idUsuario": self.idUsuario,
            "nacionalidad": self.nacionalidad,
            "nombre": self.nombre,
            "docIdentidad": self.docIdentidad,
            "telefono": self.telefono,
            "correo": self.correo
        }