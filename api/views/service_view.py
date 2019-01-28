# -*- coding: utf-8 -*-
from django.db.models import Count
import datetime
from api.Serializer.ServiceSerializer import GetServiceSerializer, ServiceSerializer
from views import *


@login_required
@api_view(['GET'])
def service_active(request):
    item_owner = Owner.get_user_from_token(request.META.get('HTTP_AUTHORIZATION'))
    try:
        item_service = Service.objects.get(owner=item_owner.pk)
        serializer = ServiceSerializer(item_service)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(dict(success=False, error=['No tienes servicios activos']),status=status.HTTP_400_BAD_REQUEST)

@login_required
@api_view(['GET', 'POST'])
def service_list(request):
    """Ver servicios activos o agregar un nuevo servicio"""
    if request.method == 'GET':
        item_dogwalker = DogWalker.get_user_from_token(request.META.get('HTTP_AUTHORIZATION'))
        response = []
        dogs_in_service = DogsServices.objects.filter(
            service__in=Service.objects.filter(dogwalker=item_dogwalker.pk)).count()
        if dogs_in_service < 3:
            items = Service.objects.filter(dogwalker__isnull=True)
            for item in items:
                count_dogs = DogsServices.objects.filter(service=item.pk).count()
                if dogs_in_service + count_dogs <= 3:
                    response.append(item)
        else:
            return Response(dict(success=False, errors=['Ya tienes el servicio completo, espera a que finalice algún '
                                                        'servicio']), status=status.HTTP_400_BAD_REQUEST)
        serializer = GetServiceSerializer(response, many=True)
        return Response(dict(success=True, data=serializer.data), status=status.HTTP_200_OK)

    elif request.method == 'POST':
        item_owner = Owner.get_user_from_token(request.META.get('HTTP_AUTHORIZATION'))
        dogwalker = request.POST.get('dogwalker','')
        try:
            Service.objects.get(owner=item_owner.pk)
            return Response(dict(success=False, errors=['Ya tienes un servicio activo']),status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        item_service = Service(owner=item_owner)

        if dogwalker != '':
            try:
                item_dogwalker = DogWalker.objects.get(pk=dogwalker)
            except:
                return Response(dict(success=False, erros=['No existe ese paseador']))
            dogs_in_service = DogsServices.objects.filter(
                service__in=Service.objects.filter(dogwalker=item_dogwalker.pk)).count()
            dogs_owner = DogOwner.objects.filter(owner=item_owner.pk).count()
            if dogs_in_service+dogs_owner > 3:
                return Response(dict(success=False, errors=['El paseador solo puede cuidar 3 perros']),status=status.HTTP_400_BAD_REQUEST)
            else:
                item_service.dogwalker=item_dogwalker
                item_service.status = 1
        item_service.save()
        items_dog = DogOwner.objects.filter(owner=item_owner.pk)
        for dog in items_dog:
            item_dog_service = DogsServices(dog=dog.dog, service=item_service)
            item_dog_service.save()
        serializer = ServiceSerializer(item_service)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@login_required
@api_view(['DELETE', 'PUT'])
def service_dogwalker(request,pk):
    """Aceptar un servicio por parte del cuidador o finalizar el servicio"""
    try:
        item_service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return Response(dict(success=False, errors=['No existe ese servicio']),status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT':
        item_dogwalker = DogWalker.get_user_from_token(request.META.get('HTTP_AUTHORIZATION'))
        item_service.dogwalker=item_dogwalker
        item_service.status = 1
        item_service.start_service = datetime.datetime.now()
        item_service.finish_service = datetime.datetime.now() + datetime.timedelta(hours=1)
        item_service.save()
        serializer = ServiceSerializer(item_service)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        item_service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





