from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import date
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
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM viajes LEFT JOIN usuarios ON viajes.usuario_id = usuarios.id"
        result = connectToMySQL(DB).query_db(query)
        return result
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM viajes LEFT JOIN usuarios ON viajes.usuario_id = usuarios.id WHERE viajes.id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        return results[0] if results else None
    @classmethod
    def update(cls, data):
        query = "UPDATE `viejo_frecuente`.`viajes` SET `destino` = %(destino)s, `fecha_inicio` = %(fecha_inicio)s, `fecha_fin` = %(fecha_fin)s, `itinerario` = %(itinerario)s, `updated_at` = NOW() WHERE id = %(id)s"
        results = connectToMySQL(DB).query_db(query, data)
        return results
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM viejo_frecuente.viajes WHERE id = %(id)s"
        results = connectToMySQL(DB).query_db(query, data)
        return results

    @staticmethod
    def validate_journey(form):
        is_valid = True
        today = date.today()
        if len(form['itinerario']) > 40:
            flash("El itinerario no puede tener más de 40 caracteres", "journey")
            is_valid = False

        if form["fecha_fin"] <= form["fecha_inicio"]:
            flash("La fecha de fin debe ser despues de la fecha de inicio.", "journey")
            is_valid = False
        if form["fecha_inicio"] < str(today):
            flash("La fecha de inicio no puede ser en el pasado.", "journey")
            is_valid = False

        return is_valid
    