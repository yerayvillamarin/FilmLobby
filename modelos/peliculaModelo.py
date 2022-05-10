class PeliculaModelo:

    def __init__(self, id, nombre, director, descripcion, anho, pais):
        self._id = id
        self._nombre = nombre
        self._director = director
        self._descripcion = descripcion
        self._anho = anho
        self._pais = pais

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def director(self):
        return self._director

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def anho(self):
        return self._anho

    @property
    def pais(self):
        return self._pais

    @staticmethod
    def get_peliculas(sirope):
        return sirope.load_all(PeliculaModelo)

    @staticmethod
    def get_pelicula_id(sirope, id):
        return sirope.find_first(PeliculaModelo, lambda pelicula: pelicula.id == id)


