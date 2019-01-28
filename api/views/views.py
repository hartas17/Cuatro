# -*- coding: utf-8 -*-

import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.utils.utils import DecodeToken
from api.models import *
from api.Serializer.DogWalkerSerializer import DogWalkerSerializer
from api.auth_middleware import login_required
from api.utils.geo_class import LatLng
logger = logging.getLogger(__name__)

class BaseView:
    pass