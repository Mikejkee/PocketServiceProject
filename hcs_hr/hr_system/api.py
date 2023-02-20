from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets

from .models import *
from .serializers import *


class AdminsViewSet(viewsets.ModelViewSet):
    serializer_class = AdministratorSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Administrator.objects.all()

        return Administrator.objects.filter(pk=pk)


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Client.objects.all()

        return Client.objects.filter(pk=pk)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Product.objects.all()

        return Product.objects.filter(pk=pk)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Order.objects.all()

        return Order.objects.filter(pk=pk)
