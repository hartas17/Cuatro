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

TODO List

```markdown
* Registrar usuarios “dueños”.
* Registrar usuarios “paseadores”.
* Un dueño puede registrar perros.
* Un dueño puede reservar a un paseador en específico.
* Un paseador puede tener un máximo de 3 perros al mismo tiempo. 
* Desde el punto de vista del paseador, puede recibir perros de multiples dueños en cada reserva.
```

Caso de uso:
```markdown
Usuario A reserva al paseador con un perro por una hora.
Usuario B reserva al paseador con dos perros por una hora.
Usuario C no puede reservar un perro con el mismo paseador hasta que pase una hora de que el usuario A o B reservaron.

```



* * *

Documentation
------------

* [Python](https://www.python.org/doc/)
* [Django](https://docs.djangoproject.com/en/2.0/)
* [Pip, Virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
