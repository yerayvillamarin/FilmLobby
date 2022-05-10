import json
import flask
import flask_login
from sirope import Sirope

from modelos.comentarioModelo import ComentarioModelo
from modelos.peliculaModelo import PeliculaModelo
from modelos.peliculaUsuarioModelo import PeliculaUsuarioModelo
from modelos.usuarioModelo import UsuarioModelo
from modelos.valoracionModelo import ValoracionModelo


def crear_app():
    app = flask.Flask(__name__)
    sirope = Sirope()
    login_manager = flask_login.login_manager.LoginManager()
    app.secret_key = "c0e5a8f0-8c7c-402a-8177-eaf68630e646"
    # app.config.from_pyfile("config.json", json.load)
    login_manager.init_app(app)

    return app, sirope, login_manager


app, sirope, login_manager = crear_app()


@login_manager.user_loader
def user_loader(alias):
    return UsuarioModelo.buscar_usuario(sirope, alias)


@login_manager.unauthorized_handler
def unauthorized():
    return "Usuario no autorizado"


# Este metodo sirve para cargar unos datos de prueba para poder probar las funcionalidades
@app.route('/cargar-datos')
def cargar_datos():

    if not UsuarioModelo.buscar_usuario(sirope, "admin"):
        sirope.save(PeliculaModelo("1", "Avatar", "James Cameron", "Está ambientada en el año 2154 y los acontecimientos que narra se desarrollan en Pandora", "2009", "Estados Unidos"))
        sirope.save(PeliculaModelo("2", "Titanic", "James Cameron", "Titanic es una película estadounidense de 1997, dramática y de catástrofe, dirigida y escrita por James Cameron", "1997", "Estados Unidos"))
        sirope.save(PeliculaModelo("3", "Steve Jobs", "Danny Boyle", "Película biográfica estadounidense de 2015, basada en la vida del cofundador de Apple, Steve Jobs, protagonizada por Michael Fassbender en el papel protagonista", "2015", "Estados Unidos"))

        sirope.save(ValoracionModelo("1", "user", "4"))

        sirope.save(ComentarioModelo("1", "Juan", "Me encanta esta película :)"))
        sirope.save(ComentarioModelo("1", "Marta", "Es buena pero me esperaba mas"))
        sirope.save(ComentarioModelo("1", "Alba", "La guardaré para ver mas tarde"))

        sirope.save(UsuarioModelo("admin", "admin@admin", "admin"))

    return flask.redirect("/")

@app.route('/')
def index():

    datos_front = {
        "usuario": UsuarioModelo.usuario_actual(),
        "peliculas": None if len(list(PeliculaModelo.get_peliculas(sirope))) == 0 else PeliculaModelo.get_peliculas(sirope)
    }
    return flask.render_template("index.html", **datos_front)

@app.route('/milista', methods=['POST', 'GET'])
def milista():
    usuario = UsuarioModelo.usuario_actual()
    if not usuario:
        return flask.redirect("/")

    if flask.request.method == 'POST':
        id_pelicula = flask.request.form.get("id_pelicula")
        alias_usuario = usuario.alias

        if id_pelicula and alias_usuario:
            pelicula_usuario = PeliculaUsuarioModelo.get_pelicula_usuario_id(sirope, id_pelicula, alias_usuario)
            if pelicula_usuario:
                sirope.delete(pelicula_usuario.__oid__)
            else:
                sirope.save(PeliculaUsuarioModelo(id_pelicula, alias_usuario))

        return flask.redirect(f"/pelicula/{id_pelicula}")
    else:
        peliculas_guardadas = PeliculaUsuarioModelo.get_peliculas_usuario(sirope, usuario)
        datos_front = {
            "usuario": usuario,
            "peliculas": peliculas_guardadas
        }

        return flask.render_template("index.html", **datos_front)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if flask.request.method == 'POST':
        alias = flask.request.form.get("alias")
        password = flask.request.form.get("password")

        errores = False

        if not alias or not password:
            errores = True

        usuario = UsuarioModelo.buscar_usuario(sirope, alias)
        if not usuario:
            errores = True
        else:
            if not usuario.comprobar_password(password):
                errores = True

        if errores:
            flask.flash("Usuario o contraseña incorrecto")
            return flask.redirect("/login")
        else:
            flask_login.login_user(usuario)
            return flask.redirect("/")
    else:
        if UsuarioModelo.usuario_actual():
            return flask.redirect("/")
        return flask.render_template("login.html")


@app.route('/registro', methods=['POST', 'GET'])
def registro():
    if flask.request.method == 'POST':
        alias = flask.request.form.get("alias")
        email = flask.request.form.get("email")
        password = flask.request.form.get("password")

        errores = False

        if not alias:
            flask.flash("El alias no puede ser vacío", "alias_error")
            errores = True
        if not email:
            flask.flash("El email no puede ser vacío", "email_error")
            errores = True
        if not password:
            flask.flash("El password no puede ser vacío", "password_error")
            errores = True

        if errores:
            return flask.redirect("/registro")

        usuario = UsuarioModelo.buscar_usuario(sirope, alias)
        if usuario:
            flask.flash("El alias ya existe", "alias_error")
            return flask.redirect("/registro")
        else:
            usuario = UsuarioModelo(alias, email, password)
            sirope.save(usuario)
            return flask.redirect("/login")

    else:
        if UsuarioModelo.usuario_actual():
            return flask.redirect("/")
        return flask.render_template("registro.html")


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect("/")


@app.route("/pelicula/<id_pelicula>")
def pelicula(id_pelicula):

    usuario = UsuarioModelo.usuario_actual()
    pelicula = PeliculaModelo.get_pelicula_id(sirope, id_pelicula)
    guardada = False
    valoracion = None
    valoracion_global = 0

    if not pelicula:
        return flask.redirect("/")

    if usuario:
        peliculas_usuarios = PeliculaUsuarioModelo.get_peliculas_usuario(sirope, usuario)
        for pelicula_usuario in peliculas_usuarios:
            if pelicula_usuario.id == pelicula.id:
                guardada = True

        valoracion_usuario = ValoracionModelo.get_valoracion_usuario(sirope, usuario.alias, id_pelicula)

        if valoracion_usuario:
            valoracion = valoracion_usuario.valoracion

    valoraciones_pelicula = ValoracionModelo.get_valoraciones_pelicula(sirope, id_pelicula)
    for valoracion_pelicula in valoraciones_pelicula:
        valoracion_global += int(valoracion_pelicula.valoracion)
    if valoracion_global != 0:
        valoracion_global = valoracion_global / len(valoraciones_pelicula)

    comentarios = ComentarioModelo.get_comentarios_pelicula(sirope, id_pelicula)


    datos_front = {
        "usuario": usuario,
        "pelicula": pelicula,
        "guardada": guardada,
        "valoracion": valoracion,
        "valoracion_global": valoracion_global,
        "comentarios": comentarios
    }
    return flask.render_template("pelicula.html", **datos_front)


@app.route('/valorar', methods=['POST'])
def valorar():
    usuario = UsuarioModelo.usuario_actual()
    if not usuario:
        return flask.redirect("/")

    id_pelicula = flask.request.form.get("id_pelicula")
    alias_usuario = usuario.alias
    valoracion = flask.request.form.get("valoracion")

    if id_pelicula and alias_usuario and valoracion:
        sirope.save(ValoracionModelo(id_pelicula, alias_usuario, valoracion))

    return flask.redirect(f"/pelicula/{id_pelicula}")


@app.route('/comentar', methods=['POST'])
def comentar():
    usuario = UsuarioModelo.usuario_actual()
    if not usuario:
        return flask.redirect("/")

    id_pelicula = flask.request.form.get("id_pelicula")
    alias_usuario = usuario.alias
    comentario = flask.request.form.get("comentario")

    if not comentario:
        flask.flash("El comentario no puede ser vacío")
        return flask.redirect(f"/pelicula/{id_pelicula}")

    if id_pelicula and alias_usuario and comentario:
        sirope.save(ComentarioModelo(id_pelicula, alias_usuario, comentario))

    return flask.redirect(f"/pelicula/{id_pelicula}")


if __name__ == '__main__':
    app.run()
