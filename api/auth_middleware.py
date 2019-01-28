# -*- coding: utf-8 -*-

from django.http import JsonResponse
from api.models import Owner, DogWalker


class AuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.owner = get_owner_from_request(request)
        request.dogwalker = get_dogwalker_from_request(request)
        return self.get_response(request)


def get_owner_from_request(request):
    """Returns the user associated with a request or None.

    Obtains the user from the token that comes in the HTTP header
    "AUTHORIZATION"
    """
    token = request.META.get("HTTP_AUTHORIZATION", "")
    return Owner.get_user_from_token(token)


def get_dogwalker_from_request(request):
    """Returns the user associated with a request or None.

    Obtains the user from the token that comes in the HTTP header
    "AUTHORIZATION"
    """
    token = request.META.get("HTTP_AUTHORIZATION", "")
    return DogWalker.get_user_from_token(token)


def login_required(func):
    """Decorator that makes sure that there is a user logged in to the
    system. Otherwise returns a json message with a 401 status_code"""

    def wrapped_func(request, *args, **kwargs):
        if request.owner is None and request.dogwalker is None:
            response = {'success': False,
                        'errors': ["Se necesita iniciar sesion " +
                                   "para usar este metodo"],
                        'status': 401}
            return JsonResponse(response, status=401, safe=False)
        else:
            return func(request, *args, **kwargs)

    # return the actual function
    return wrapped_func


def login_and_is_owner(func):
    """Decorator that makes sure that there is a user logged in to the
    system. Otherwise returns a json message with a 401 status_code"""

    def wrapped_func(request, *args, **kwargs):
        if request.owner is not None:
            try:
                if int(kwargs["pk"]) == int(request.owner.pk):
                    pass
                else:
                    response = {'success': False,
                                'errors': ["No eres propietario de estos datos"],
                                'status': 401}
                    return JsonResponse(response, status=401, safe=False)
            except :
                 response = {'success': False,
                        'errors': ["Se necesita iniciar sesion " +
                                   "para usar este metodo"],
                        'status': 401}
            return JsonResponse(response, status=401, safe=False)
        if request.owner is None and request.dogwalker is None:
            response = {'success': False,
                        'errors': ["Se necesita iniciar sesion " +
                                   "para usar este metodo"],
                        'status': 401}
            return JsonResponse(response, status=401, safe=False)
        else:
            return func(request, *args, **kwargs)

    # return the actual function
    return wrapped_func


#Check if user is dogwalker
def is_dogwalker(func):
    def wrapped_func(request, *args, **kwargs):
        if request.dogwalker is None:
            response = {'success': False,
                        'errors': ["Se necesita iniciar sesion " +
                                   "para usar este metodo"],
                        'status': 401}
            return JsonResponse(response, status=401, safe=False)
        else:
            return func(request, *args, **kwargs)

    # return the actual function
    return wrapped_func


#Check if user is owner
def is_owner(func):
    def wrapped_func(request, *args, **kwargs):
        if request.dogwalker is None:
            response = {'success': False,
                        'errors': ["Se necesita iniciar sesion " +
                                   "para usar este metodo"],
                        'status': 401}
            return JsonResponse(response, status=401, safe=False)
        else:
            return func(request, *args, **kwargs)

    return wrapped_func
