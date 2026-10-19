from flask import flash, redirect, render_template, request, session
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    if not Usuario.validate_register(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
    data = {**request.form, "password": pw_hash}
    session["usuario_id"] = Usuario.save(data)
    return redirect("/dashboard")


@app.route("/login", methods=["POST"])
def login():
    user = Usuario.get_by_email(request.form)

    if not user:
        flash("E-mail no registrado", "login")
        return redirect("/")

    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Password incorrecto", "login")
        return redirect("/")

    session["usuario_id"] = user.id
    print("User logined!")
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    user = Usuario.get_one({"id": session["usuario_id"]})
    if not user:
        return redirect("/")
    return render_template("dashboard.html", user=user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")