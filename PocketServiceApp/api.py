from django.http import JsonResponse
from rest_framework import viewsets
from celery.result import AsyncResult

from .models import *
from .serializers import *


class AdminsViewSet(viewsets.ModelViewSet):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #
    #     # Задача в celery
    #     task = api_tasks.create_order.delay(serializer.data)
    #
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)


def task_status(request):
    task_id = request.GET.get('task_id')

    if task_id:
        task = AsyncResult(task_id)
        if task.state == 'FAILURE':
            error = str(task.result)
            response = {
                'state': task.state,
                'error': error,
            }
        else:
            response = {
                'state': task.state,
            }
        return JsonResponse(response)
