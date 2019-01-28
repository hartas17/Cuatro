# -*- coding: utf-8 -*-
from api.Serializer.DogOwnerSerializer import DogOwnerSerializer, DogSerializer, GetDogOwnerSerializer
from views import *


@login_required
@api_view(['GET', 'POST'])
def dog_owner(request):
    """Ver la lista de relación perro con dueño"""
    item_owner = Owner.get_user_from_token(request.META.get('HTTP_AUTHORIZATION'))
    if request.method == 'GET':
        items = DogOwner.objects.filter(owner=item_owner.pk)
        serializer = DogOwnerSerializer(items,many=True)
        return Response(dict(success=True, data=serializer.data),status=status.HTTP_200_OK)
    elif request.method == 'POST':
        pass


@login_required
@api_view(['POST','GET'])
def dog_list(request):
    """Administración de perros"""
    item_owner = Owner.get_user_from_token(request.META.get('HTTP_AUTHORIZATION'))
    if request.method == 'POST':
        serializer = DogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dog = Dog.objects.get(pk=serializer.data['id'])
            item = DogOwner(owner=item_owner,dog=dog)
            item.save()
            serializer_dog = GetDogOwnerSerializer(item)
            return Response(serializer_dog.data,status=status.HTTP_200_OK)
        else:
            return Response(dict(success=False, errors=[serializer.errors]),status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        items = DogOwner.objects.filter(owner=item_owner.pk)
        serializer = GetDogOwnerSerializer(items,many=True)
        return Response(dict(success=True, data=serializer.data),status=status.HTTP_200_OK)