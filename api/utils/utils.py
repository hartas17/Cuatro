# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import os
from pyfcm import FCMNotification

from rest_framework_jwt import utils


from api.models import AppUsers, PanelUsers, Users, DataDevice

logger = logging.getLogger(__name__)


from django.core.validators import validate_email


def check_errors_password(password):
    """Revisa las condiciones de una buena contraseña y devuelve una
    lista de errores."""
    errors = []
    if len(password) < 6:
        errors.append("La contraseña debe tener al menos 6 caracteres")
    return errors


def check_errors_email(email, errors):
    """Checks that a given email is a valid email

    email - email to validate
    errors (out)
    """
    result = True
    try:
        validate_email(email)
    except:
        errors.append("El email que se uso no es valido")
        result = False
    return result


def check_errors_create_account(username, firstname, email, password, type):
    errors = []

    username_query = Users.objects.filter(username=username)
    email_query = Users.objects.filter(email=username)

    if not username and(username_query.count() >= 1):
        errors.append("Ese usuario ya está vinculado a otra cuenta")


    if not email:
        errors.append("Se necesita proporcionar un correo electrónico")

    if email and (email_query.count() >= 1):
        errors.append("Ese correo ya está vinculado a otra cuenta")

    if (not errors) and email:
        check_errors_email(email, errors)

    errors.extend(check_errors_password(password))

    return errors


def check_errors_login(username, password):
    errors = []

    if not username:
        errors.append("No se especifico el nombre de usuario")

    if not password:
        errors.append(u"No se especifico la contraseña")

    return errors


def handle_uploaded_file(file, filename, route):
    #route='media/profile/'
    if not os.path.exists(route):
        os.mkdir(route)
    with open(route+ filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def DecodeToken(request):
    Token = request.META.get('HTTP_AUTHORIZATION')
    token = utils.jwt_decode_handler(Token)
    print token
    try:
        item = AppUsers.objects.get(pk=token['user_id'])
        return item
    except Exception as e:
        print e
        return None


def send_push(token,message_title,message_body):
    push_service = FCMNotification(
        api_key='AAAA68GdzDs:APA91bFce3Ca1y79C3d3RDTjaKNQhET7kzeRbC8ljVSf4uPNeq5G974K9j6WEn3SUPkY0gls6PfblO4oIk0mOauAVXfME77mCAsmFdodOx246KJOwMaxBW8_ZM1OnenI-4IwJ8dz4gbW')

    # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

    registration_id = token
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                               message_body=message_body)
    logging.debug(result)
    pass


def send_push_all(message_title,message_body):
    push_service = FCMNotification(
        api_key='AAAA68GdzDs:APA91bFce3Ca1y79C3d3RDTjaKNQhET7kzeRbC8ljVSf4uPNeq5G974K9j6WEn3SUPkY0gls6PfblO4oIk0mOauAVXfME77mCAsmFdodOx246KJOwMaxBW8_ZM1OnenI-4IwJ8dz4gbW')

    # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

    registration_id = DataDevice.objects.all()
    response =[]
    for registration in registration_id:
        response.append(registration.token)
    print response
    result = push_service.notify_multiple_devices(registration_ids=response, message_title=message_title,
                                               message_body=message_body)
    logging.debug(result)
    pass