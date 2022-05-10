from modelos.peliculaModelo import PeliculaModelo


class PeliculaUsuarioModelo:

    def __init__(self, id_pelicula, alias_usuario):
        self._id_pelicula = id_pelicula
        self._alias_usuario = alias_usuario

    @property
    def id_pelicula(self):
        return self._id_pelicula

    @property
    def alias_usuario(self):
        return self._alias_usuario

    @staticmethod
    def get_peliculas_usuario(sirope, usuario):
        peliculas_usuarios = sirope.load_all(PeliculaUsuarioModelo)
        peliculas = PeliculaModelo.get_peliculas(sirope)
        peliculas_guardadas = list()

        for pelicula in peliculas:
            peliculas_usuarios = sirope.load_all(PeliculaUsuarioModelo)
            for pelicula_usuario in peliculas_usuarios:
                if pelicula.id == pelicula_usuario.id_pelicula and usuario.alias == pelicula_usuario.alias_usuario:
                    peliculas_guardadas.append(pelicula)

        return peliculas_guardadas

    @staticmethod
    def get_pelicula_usuario_id(sirope, id_pelicula, alias_usuario):
        return sirope.find_first(PeliculaUsuarioModelo, lambda pelicula_usuario: pelicula_usuario.id_pelicula == id_pelicula and pelicula_usuario.alias_usuario == alias_usuario)
