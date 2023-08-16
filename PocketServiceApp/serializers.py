from rest_framework import serializers
from .models import *


class PatchModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(PatchModelSerializer, self).__init__(*args, **kwargs)

class RoleSerializer(PatchModelSerializer):

    class Meta:
        model = Role
        fields = ['role_type']

class PersonSerializer(PatchModelSerializer):
    role = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = '__all__'

class AdministratorSerializer(PatchModelSerializer):
    role = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Administrator
        fields = '__all__'


class ClientSerializer(PatchModelSerializer):
    role = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = '__all__'


class ProductSerializer(PatchModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(PatchModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
