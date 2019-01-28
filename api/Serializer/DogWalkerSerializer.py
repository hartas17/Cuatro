from rest_framework.serializers import ModelSerializer

from api.models import DogWalker


class DogWalkerSerializer(ModelSerializer):
    class Meta:
        model = DogWalker
        depth = 0
        fields = '__all__'


class GetDogWalkerSerializer(ModelSerializer):
    class Meta:
        model = DogWalker
        exclude = ('password', 'token', 'updated')
        depth = 1