from flask import flash, redirect, render_template, request, session
from flask_app.models.usuario import Usuario
from flask_app.models.viaje import Viaje
from flask_app import app

@app.route("/nuevo")
def nuevo_viaje():
    if "usuario_id" not in session:
        return redirect("/")
    user = Usuario.get_one({"id": session["usuario_id"]})
    if not user:
        return redirect("/")
    return render_template("nuevo_viaje.html")

@app.route("/agregar_viaje", methods=["POST"])
def agregar_viaje():
    data = {**request.form, "usuario_id": session["usuario_id"]}
    Viaje.save(data)

    return redirect("/dashboard")

@app.route("/ver/<int:id>")

def ver_viaje(id):
    if "usuario_id" not in session:
        return redirect("/")
    user = Usuario.get_one({"id": session["usuario_id"]})
    if not user:
        return redirect("/")
    data = {
        "id": id
    }
    viaje = Viaje.get_by_id(data)
    return render_template("ver_viaje.html", viaje = viaje)