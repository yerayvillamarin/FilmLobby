import flask_login
from werkzeug.security import generate_password_hash, check_password_hash


class UsuarioModelo(flask_login.UserMixin):

    def __init__(self, alias, email, password):
        self._alias = alias
        self._email = email
        self._password = generate_password_hash(password)

    @property
    def alias(self):
        return self._alias

    @property
    def email(self):
        return self._email

    def comprobar_password(self, password):
        return check_password_hash(self._password, password)

    def get_id(self):
        return self._alias

    @staticmethod
    def usuario_actual():
        usuario = flask_login.current_user

        if usuario.is_anonymous:
            flask_login.logout_user()
            usuario = None

        return usuario

    @staticmethod
    def buscar_usuario(sirope, alias):
        return sirope.find_first(UsuarioModelo, lambda usuario: usuario.alias == alias)
