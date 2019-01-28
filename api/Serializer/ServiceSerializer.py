# -*- coding: utf-8 -*-

from rest_framework.serializers import ModelSerializer

from api.Serializer.OwnserSerializer import OwnerSerializer, GetOwnerSerializer
from api.models import Service


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        depth = 0
        fields = '__all__'


class GetServiceSerializer(ModelSerializer):
    owner = GetOwnerSerializer()

    class Meta:
        model = Service
        depth = 1
        fields = '__all__'
