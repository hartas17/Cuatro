# -*- coding: utf-8 -*-

from api.Serializer.DogWalkerSerializer import GetDogWalkerSerializer
from views import *


@login_required
@api_view(['GET', 'POST'])
def dogwalker_list(request):
    item_user = Owner.get_user_from_token(request.META.get('HTTP_AUTHORIZATION'))
    if request.method == 'GET':
        items = DogWalker.objects.all()
        response = []
        for dog_walker in items:
            total_services = DogsServices.objects.filter(
                service__in=Service.objects.filter(dogwalker=dog_walker.pk)).count()
            if total_services < 3:
                try:
                    Favorite.objects.get(owner=item_user.pk, dogwalker=dog_walker.pk)
                    dog_walker.favorite = True
                except Exception as e:
                    dog_walker.favorite = False
                    logger.error(e)
                response.append(dog_walker)
        serializer = GetDogWalkerSerializer(response, many=True)
        return Response(dict(success=True, data=serializer.data), status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = DogWalkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@login_required
@api_view(['GET', 'PUT', 'DELETE'])
def dogwalker_detail(request, pk):
    try:
        item = DogWalker.objects.get(pk=pk)
    except DogWalker.DoesNotExist:
        return Response(dict(success=False, errors=['No existe ese cuidados']), status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = GetDogWalkerSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = DogWalkerSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            Response(dict(success=False, errors=[serializer.errors]), status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@login_required
@api_view(['POST'])
def dogwalker_favorite(request):
    item_owner = Owner.get_user_from_token(request.META.get('HTTP_AUTHORIZATION'))
    dogwalker = request.POST.get('dogwalker', )

    try:
        item_dogwalker = DogWalker.objects.get(pk=dogwalker)
        items = Favorite.objects.filter(owner=item_owner, dogwalker=item_dogwalker)
        if len(items)>0:
            return Response(dict(success=False, errros=['Ese cuidador ya está en favoritos']), status=status.HTTP_400_BAD_REQUEST)
        item = Favorite(owner=item_owner, dogwalker=item_dogwalker)
        item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(e)
        return Response(dict(success=False, errros=['No existe ese cuidador']), status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['DELETE'])
def dogwalker_delete(request, pk):
    item_owner = Owner.get_user_from_token(request.META.get('HTTP_AUTHORIZATION'))
    try:
        item = Favorite.objects.get(owner=item_owner.pk, dogwalker=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(e)
        return Response(dict(success=False, errros=['Ese cuidador no está en favoritos']), status=status.HTTP_400_BAD_REQUEST)


def find_object(lat, lng, radius, sort_by):
    center = LatLng(lat, lng)

    max_lat = center.destination_point_north(radius).lat
    min_lat = center.destination_point_south(radius).lat
    max_lng = center.destination_point_east(radius).lng
    min_lng = center.destination_point_west(radius).lng

    # find all objects inside the given rectangle

    objects = Location.objects.filter(
        lat__lte=max_lat,
        lat__gte=min_lat,
        lng__lte=max_lng,
        lng__gte=min_lng).all()

    # function that returns the distance from the object to the
    # center point
    distance_to_center = lambda st: center.distance_to(st.get_location())
    # function that returns true if the object is within the
    # radius
    is_within_radius = lambda st: (distance_to_center(st) <= radius)

    objects = filter(is_within_radius, objects)

    # Sort object by given parameter

    objects = list(objects)

    return objects
