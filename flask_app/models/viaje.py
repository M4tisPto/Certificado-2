from flask_app.config.mysqlconnection import connectToMySQL
DB = "viejo_frecuente"

class Viaje:
    def __init__(self, data):
        self.id = data["id"]
        self.destino = data["destino"]
        self.fecha_inicio = data["fecha_inicio"]
        self.fecha_fin = data["fecha_fin"]
        self.itinerario = data["itinerario"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.usuario_id = data["usuario_id"]


    @classmethod
    def save(cls, data):
        query = "INSERT INTO viajes (destino, fecha_inicio, fecha_fin, itinerario, created_at, updated_at, usuario_id) VALUES (%(destino)s, %(fecha_inicio)s, %(fecha_fin)s, %(itinerario)s, NOW(), NOW(), %(usuario_id)s)"
        result = connectToMySQL(DB).query_db(query, data)
        return result
    