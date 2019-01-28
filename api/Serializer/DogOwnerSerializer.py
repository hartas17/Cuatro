# -*- coding: utf-8 -*-

from rest_framework.serializers import ModelSerializer

from api.Serializer.OwnserSerializer import OwnerSerializer, GetOwnerSerializer
from api.models import DogOwner, Dog


class DogOwnerSerializer(ModelSerializer):
    class Meta:
        model = DogOwner
        depth = 0
        fields = '__all__'


class GetDogOwnerSerializer(ModelSerializer):
    owner = GetOwnerSerializer()

    class Meta:
        model = DogOwner
        depth = 1
        fields = '__all__'


class DogSerializer(ModelSerializer):
    class Meta:
        model = Dog
        depth = 0
        fields = '__all__'

