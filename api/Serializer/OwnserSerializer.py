from rest_framework.serializers import ModelSerializer

from api.models import Owner


class OwnerSerializer(ModelSerializer):
    class Meta:
        model = Owner
        depth = 0
        fields = '__all__'


class GetOwnerSerializer(ModelSerializer):
    class Meta:
        model = Owner
        exclude = ('password', 'token', 'updated')
        depth = 1