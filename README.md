# FilmLobby
Aplicación web realizada en Python 3 usando el Microframework Flask


## Datos de prueba
Para poder probar las funcionalidades de la aplicación se ha creado un método que genera datos de prueba en la aplicación para tener una base.
Este método se puede ejecutar en la ruta ___/cargar-datos___


```
http://dominio/cargar-datos
```
Esto creará 3 películas, en una de ellas se agregaran comentarios y puntuaciones.

También creará el usuario admin/admin


## Requisitos
- Python 3
- Flask
- Flask_login
- Sirope
- Base de datos Redis


## Funcionamiento
La Base de Datos Redis debe de estar escuchando en localhost:6379

Las pruebas se han realizado desde el servidor web de PyCharm
