class ValoracionModelo:

    def __init__(self, id_pelicula, alias_usuario, valoracion):
        self._id_pelicula = id_pelicula
        self._alias_usuario = alias_usuario
        self._valoracion = valoracion

    @property
    def id_pelicula(self):
        return self._id_pelicula

    @property
    def alias_usuario(self):
        return self._alias_usuario

    @property
    def valoracion(self):
        return self._valoracion

    @staticmethod
    def get_valoracion_usuario(sirope, alias_usuario, id_pelicula):
        return sirope.find_first(ValoracionModelo, lambda valoracion_usuario: valoracion_usuario.id_pelicula == id_pelicula and valoracion_usuario.alias_usuario == alias_usuario)

    @staticmethod
    def get_valoraciones_pelicula(sirope, id_pelicula):
        valoraciones = sirope.load_all(ValoracionModelo)
        valoraciones_pelicula = list()

        for valoracion in valoraciones:
            if valoracion.id_pelicula == id_pelicula:
                valoraciones_pelicula.append(valoracion)

        return valoraciones_pelicula
