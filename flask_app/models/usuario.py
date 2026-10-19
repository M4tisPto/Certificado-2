import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
DB = "viejo_frecuente"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')


class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO usuarios (nombre, apellido, email, password, created_at, updated_at) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s, NOW(), NOW())"
        result = connectToMySQL(DB).query_db(query, data)
        return result
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)
        return cls(result[0]) if result else None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios"
        results = connectToMySQL(DB).query_db(query)
        return [cls(result) for result in results] if results else []
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM usuario WHERE email = %(email)s"
        results = connectToMySQL(DB).query_db(query, data)
        if len(results) == 1:
            user = cls(results[0])
            return user
        else:
            return False
        
    @staticmethod
    def validate_register(form):
        is_valid = True
        if len(form['nombre']) < 2:
            flash("El nombre debe tener al menos 2 caracteristicas.", "register")
            is_valid = False

        if len(form["apellido"]) < 2:
            flash("El apellido debe tener al menos 2 caracteristicas.", "register")
            is_valid = False

        if not EMAIL_REGEX.match(form['email']):
            flash("E-mail invalido.", "register")
            is_valid = False
        if form['password'] != form["confirm_pw"]:
            flash("Las contraseñas no coinciden", "register")
            is_valid = False

        return is_valid
    