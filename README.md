Dogger Project
========================================

About
-----
Dogger
El objetivo de la app es conectar “dueños” de perros con “paseadores” de perros. 


Prerequisites
-------------
- pip
- virtualenv (virtualenvwrapper is recommended)
- Python >= 2.7
- Mysql

Installation
------------

Ubuntu 18.04

Packages
```
$ sudo apt-get install python-pip
$ sudo apt install mysql-client
$ sudo apt install python-mysqldb
$ sudo apt-get install libmysqlclient-dev
$ sudo apt install python-dev libpython-dev
$ sudo apt-get install supervisor
$ sudo apt install virtualenv

```

Set settings locales

```
$ cp settings.py.example settings.py
```

Environment

```
# Install virtualenv
$ virtualenv -p python venv

# Activate virturalenv
$ source venv/bin/activate
```

Install requeriments

```
$ pip install -r requeriments.txt
```


Run migrations

```
$ python manage.py makemigrations
$ python manage.py migrate
```


Run local
```
$ python manage.py runserver
```

## Acceso a la API:

# [API documentation](https://documenter.getpostman.com/view/2930473/Rztitq4V)

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/0622c73e391d26fa1d8d)
# COLLECTION
[descargar la collection](https://www.getpostman.com/collections/0622c73e391d26fa1d8d) funciona en [POSTMAN](https://www.getpostman.com/postman)


##  Consideraciones del proyecto:
```markdown
* El usuario propietario del perro puede administrar su perfil, incluido foto
* El paseador de perro puede administrar perfil, incuido foto
* Se puede cambiar contraseña
* Se puede recuperar contraseña
* Se pueden agregar perros al propietario
* Se puede agregar a favoritos a algún paseador
* Se puede reservar el paseador para cuidar mis perros
* Se puede visualizar los paseadores activos y que cumplen con 
las caracteristivos del servicio que requiero(cantidad de perros con los que cuento)

```

 
TODO List

```markdown
* Poder seleccionar los perros que quiero que paseen, esto en caso que tenga más de 3 perros
* Agregar precio al servicio
* Filtrar servicios activos por geolocalización
* Visualizar por geolocalizacion en que lugar se encuentra mi perro y su cuidador
* El aceptar un servicio pasar por 2 estados, primero servicio aceptado y luego servicio iniciado
* Finalizar servicio sin eliminarlo. Esto para mantener registro de sus status
* Agregar status de actividad a paseadores para poder ponerse en status de inactivo
```

Caso de uso funcionales:
```markdown
*
Usuario A reserva al paseador con un perro por una hora.
Usuario B reserva al paseador con dos perros por una hora.
Usuario C no puede reservar un perro con el mismo paseador hasta que pase una hora de que el usuario A o B reservaron.

*
Paseador A tiene 2 perros a su cuidado Paseador B tiene 1 perro. Si el Usuario C Tiene 2 perros para que le cuiden, al
bucar Paseadores, solamente le mostrará el Paseador B. Ya que es el único que tiene cupo para cuidar sus 2 perros

* 
Puedo agregar paseadores a favoritos, se refleja en la lista de paseadores activos

*
No puedes tener más de un servicio activo

*
Valida que al intentar reservar un paseador no tenga ya 3 perros en sus servicio o que la suma de los que tiene 
más los que yo tengo no sea mayor que 3

```



* * *

Documentation
------------

* [Python](https://www.python.org/doc/)
* [Django](https://docs.djangoproject.com/en/2.0/)
* [Pip, Virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
