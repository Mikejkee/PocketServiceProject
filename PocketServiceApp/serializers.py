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

class ProductSerializer(PatchModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

class AreaSerializer(PatchModelSerializer):

    class Meta:
        model = Area
        fields = '__all__'

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

class CompanySerializer(PatchModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class ClientSerializer(PatchModelSerializer):
    role = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = '__all__'

class AgentSerializer(PatchModelSerializer):
    role = RoleSerializer(many=True, read_only=True)
    product = ProductSerializer(many=True, read_only=True)
    area = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Agent
        fields = '__all__'


class OrderSerializer(PatchModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class PriceSerializer(PatchModelSerializer):
    product = ProductSerializer(many=True, read_only=True)
    agent = AgentSerializer(many=True, read_only=True)

    class Meta:
        model = Price
        fields = '__all__'


class SpecializationSerializer(PatchModelSerializer):

    class Meta:
        model = Specialization
        fields = '__all__'


class UniversitySerializer(PatchModelSerializer):

    class Meta:
        model = University
        fields = '__all__'


class EducationSerializer(PatchModelSerializer):
    agent = AgentSerializer(many=True, read_only=True)
    specialization = SpecializationSerializer(many=True, read_only=True)
    university = UniversitySerializer(many=True, read_only=True)

    class Meta:
        model = Education
        fields = '__all__'


class CommentSerializer(PatchModelSerializer):
    agent = AgentSerializer(many=True, read_only=True)
    client = ClientSerializer(many=True, read_only=True)
    order = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'