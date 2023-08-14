from rest_framework import serializers
from .models import *


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['role_type']

class PersonSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=True)

    class Meta:
        model = Person
        fields = '__all__'

class AdministratorSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=True)

    class Meta:
        model = Administrator
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=True)

    class Meta:
        model = Client
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
