# -*- coding: utf-8 -*-
import logging
import base64

from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.auth_middleware import login_required
from api.models import Users, Owner, DogWalker
from api.utils.utils import handle_uploaded_file, check_errors_login, DecodeToken

logger = logging.getLogger(__name__)


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


def check_errors_create_account(username, firstname, email, password):
    errors = []
    username_query = Users.objects.filter(username=username)
    email_query = Users.objects.filter(email=email)

    if not username and (username_query.count() >= 1):
        errors.append("Ese usuario ya está vinculado a otra cuenta")

    if not email:
        errors.append("Se necesita proporcionar un correo electrónico")

    if email and (email_query.count() >= 1):
        errors.append("Ese correo ya está vinculado a otra cuenta")

    if (not errors) and email:
        check_errors_email(email, errors)

    errors.extend(check_errors_password(password))

    return errors


@api_view(['POST'])
def register_owner(request):
    if request.method == 'POST':
        request.POST._mutable = True
        name = ""
        try:
            myfile = request.FILES["image"]
            handle_uploaded_file(myfile, myfile.name, 'media/profile/')
            name = "/profile/" + myfile.name
        except Exception as e:
            print e
            name = '/profile/defaul.png'
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        errors = check_errors_create_account(email, firstname, email, password, 1)

        status = 400
        response = {'success': (len(errors) == 0),
                    'errors': errors}

        if response['success']:
            # successs
            status = 200
            new_user = Owner(username=email, firstname=firstname, lastname=lastname, email=email,image=name)
            new_user.set_password(password)
            response = new_user.details_dict()
        else:
            logger.error(errors)

            # We return the response
            # We need to use unsafe mode to return a list of errors
        return JsonResponse(response, safe=False, status=status, content_type='application/json')


@api_view(['POST'])
def login_app_user(request):
    if request.method == 'POST':
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        errors = check_errors_login(email, password)
        user = Owner.objects.filter(username=email).first()
        status = 200
        # check that that the account exists
        if (not errors) and (user is None):
            # username does not exist
            errors.append("Usuario no encontrado")

        # check password matches
        if not errors:

            if not user.check_password(password):
                errors.append("Contraseña incorrecta")

        # check that the email has been confirmed
        #    if not errors and user.email == "":
        #        errors.append("Se necesita confirmar el email" +
        #                      " de la cuenta para iniciar sesión")
        if not errors:
            # Success
            response = user.details_dict()
        else:
            # Error
            status = 400
            response = {'success': False,
                        'errors': errors}

        return JsonResponse(response, safe=False, status=status)
    return None


@api_view(['POST'])
def register_dogwalker(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        errors = check_errors_create_account(email, firstname, email, password, 2)

        status = 400
        response = {'success': (len(errors) == 0),
                    'errors': errors}

        if response['success']:
            # successs
            status = 200
            new_user = DogWalker(username=email, firstname=firstname, lastname=lastname, email=email)
            new_user.set_password(password)
            response['data'] = new_user.details_dict()
        else:
            logger.error(errors)

            # We return the response
            # We need to use unsafe mode to return a list of errors
        return JsonResponse(response, safe=False, status=status, content_type='application/json')


@api_view(['POST'])
def login_panel_user(request):

    email = request.POST.get("email", "")
    password = request.POST.get("password", "")
    print email
    print password
    errors = check_errors_login(email, password)
    user = DogWalker.objects.filter(username=email).first()
    status = 200
    # check that that the account exists
    if (not errors) and (user is None):
        # username does not exist
        errors.append("Usuario no encontrado")

    # check password matches
    if not errors:

        if not user.check_password(password):
            errors.append("Contraseña incorrecta")

    # check that the email has been confirmed
    #    if not errors and user.email == "":
    #        errors.append("Se necesita confirmar el email" +
    #                      " de la cuenta para iniciar sesión")
    if not errors:
        # Success
        response = {'success': True,
                    'data': user.details_dict()}
    else:
        # Error
        status = 400
        response = {'success': False,
                    'errors': errors}

    return Response(response,status=status)


@login_required
@api_view(['POST'])
def change_password(request):
    try:
        item_user = DecodeToken(request)
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        if item_user.check_password(old_password):
            item_user.set_password(new_password)
            item_user.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(dict(success=False, errors=['No coinciden las contraseñas']),
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print e
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def recover_password(request):
    if request.method == 'POST':
        request.POST._mutable = True
        email = request.data["email"]
        try:
            item_app_user = Users.objects.get(email__iexact=request.data['email'])
            data = base64.b64encode(request.data['email'])
            item_app_user.recoverPassword=data
            send_mail('Recuperar contrasena', "http://localhost:8000/api/reset_password/?token=" + data,
                      'hartas17@gmail.com', [email],
                      fail_silently=False)
        except Exception as e:
            logging.debug(e)
            print e
        return Response(status=200)


class PasswordResetView(View):
    """HTML based view to reset a password."""
    http_allowed_methods = ['get', 'post']

    template = "dogger/password-reset.html"
    success = "dogger/success_password.html"
    error_page = "dogger/error_password.html"

    def get(self, request):
        """Displays the password reset token with the appropiate token"""
        context = {'token': request.GET.get("token", "")}

        return render(request, self.template, context)

    def post(self, request):
        """Validates info and tries to reset the password"""
        token_message = ""
        new_password = request.POST.get("new_password", "")
        new_password_verify = request.POST.get("new_password_verify", "")
        if new_password == new_password_verify:
            try:
                token_message = request.POST.get("token", "")
                email = base64.b64decode(token_message)
                context = {'success': True}
                usuario = AppUsers.objects.get(email=email)
                usuario.password = make_password(new_password)
                if usuario.recoverpassword==token_message:
                    usuario.recoverpassword=""
                    usuario.save()
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                return render(request, self.success, context)
            except Exception as e:
                logger.error(e)
                context = {'success': False}
                return render(request, self.error_page, context)
        print new_password

        errors = []

        if new_password != new_password_verify:
            context = {'success': True}
            return render(request, self.template, context)
        if not errors:
            context = {'success': False}

            return render(request, self.template, context)

        if not errors:
            ## Redirect to success page
            ## TODO
            context = {'success': True}

            return render(request, self.template, context)


        else:
            # Redisplay the page with error messages
            context = {'token': token_message,
                       'errors': errors}
            return render(request, self.template, context)