def RegistrarRutasUsuario(app):

    @app.route('/clientes', methods=['POST'])
    def get_users():
        # lógica para obtener usuarios
        return {"clientes": []}
    
    @app.route('/clientes/<int:id>', methods=['GET'])
    def get_user(id):
        # lógica para obtener usuario por id
        return {"cliente_id": id}
