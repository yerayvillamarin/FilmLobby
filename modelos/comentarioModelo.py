class ComentarioModelo:

    def __init__(self, id_pelicula, alias_usuario, comentario):
        self._id_pelicula = id_pelicula
        self._alias_usuario = alias_usuario
        self._comentario = comentario

    @property
    def id_pelicula(self):
        return self._id_pelicula

    @property
    def alias_usuario(self):
        return self._alias_usuario

    @property
    def comentario(self):
        return self._comentario

    @staticmethod
    def get_comentarios_pelicula(sirope, id_pelicula):
        comentarios = sirope.load_all(ComentarioModelo)
        comentarios_pelicula = list()

        for comentario in comentarios:
            if comentario.id_pelicula == id_pelicula:
                comentarios_pelicula.append(comentario)

        return comentarios_pelicula
