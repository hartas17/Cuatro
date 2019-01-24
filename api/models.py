# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
import datetime as times

from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from rest_framework_jwt import utils
from rest_framework_jwt.settings import api_settings


# Create your models here.


class Users(models.Model):
    username = models.CharField(unique=True, max_length=255)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    image = models.CharField(max_length=255, null=True, blank=True)
    firstname = models.CharField(max_length=124)
    lastname = models.CharField(max_length=124, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=128)
    token = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(db_column='created', auto_now_add=True)
    updated = models.DateTimeField(db_column='updated', auto_now=True)

    class Meta:
        managed = True
        db_table = 'Users'

    def set_password(self, password):
        self.password = make_password(password)
        self.save()

    def check_password(self, password):
        """Returns true if this is the user's password, false
        otherwise """
        return check_password(password, self.password)

    def create_token(self):
        """Creates a signed token that identifies the current user and
        expires in an hour
        """
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        api_settings.JWT_EXPIRATION_DELTA = times.timedelta(days=365)
        token = ""
        try:
            user = self
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

        except Exception as e:
            print e
        return token


class Owner(Users):

    class Meta:
        managed = True
        db_table = 'owner'

    def details_dict(self):
        self.token = self.create_token()
        self.save()
        return {'id': self.pk,
                'username': self.username,
                'firstname': self.firstname,
                'email': self.email,
                'token': self.token
                }

    @classmethod
    def get_user_from_token(self, Token):
        userid = -1

        # get user id
        try:
            token = utils.jwt_decode_handler(Token)
            item = Owner.objects.get(pk=token['user_id'])
            if item.email == token['email']:
                userid = token['user_id']

            else:
                userid = -1
        except:
            pass

        # get user
        # if userid != -1:
        user = Owner.objects.filter(id=userid).first()

        return user


class DogWalker(Users):
    reserved = models.BooleanField(default=False)
    ranking = models.BooleanField(default=5.0)


    class Meta:
        managed = True
        db_table = 'dog_walker'

    def details_dict(self):
        self.token = self.create_token()
        self.save()
        return {'id': self.pk,
                'username': self.username,
                'firstname': self.firstname,
                'email': self.email,
                'token': self.token
                }

    @classmethod
    def get_user_from_token(self, Token):
        userid = -1

        # get user id
        try:
            token = utils.jwt_decode_handler(Token)
            item = DogWalker.objects.get(pk=token['user_id'])
            if item.email == token['email']:
                userid = token['user_id']

            else:
                userid = -1
        except:
            pass

        # get user
        # if userid != -1:
        user = DogWalker.objects.filter(id=userid).first()

        return user


class Dog(models.Model):
    """En caso de que dos razas no sean compatibles, para eso se crea tipo de dato Choice"""
    A = "PA"
    B = "CH"
    C = "PT"
    D = "LA"
    TYPE_DOG_CHOICE = (
        (A, 'Pastor Aleman'),
        (B, 'Chihuhua'),
        (C, 'Pitbull'),
        (D, 'Labrador'),
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=2, choices=TYPE_DOG_CHOICE)
    created = models.DateTimeField(db_column='created', auto_now_add=True)
    updated = models.DateTimeField(db_column='updated', auto_now=True)

    class Meta:
        managed = True
        db_table = 'dog'


class DogOwner(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(db_column='created', auto_now_add=True)
    updated = models.DateTimeField(db_column='updated', auto_now=True)

    class Meta:
        managed = True
        db_table = 'dog_owner'


class Reserver(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True, blank=True)
    dogwalker = models.ForeignKey(DogWalker, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(db_column='created', auto_now_add=True)
    updated = models.DateTimeField(db_column='updated', auto_now=True)

    class Meta:
        managed = True
        cb_table = 'reserver'


class Location(models.Model):
    """Tanto cuidador como usuario deben tener localizacion para saber si puede cumplir el encargo"""
    lat = models.FloatField(blank=True, null=False)
    lng = models.FloatField(blank=True, null=False)
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, blank=True, null=True)
    createdat = models.DateTimeField(db_column='created_at', auto_now_add=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updated_at', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'location'

