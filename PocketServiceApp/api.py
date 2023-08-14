from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from celery.result import AsyncResult
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import *
from .serializers import *


TELEGRAM_ID_QUERY = openapi.Parameter('TelegramId', in_=openapi.IN_QUERY,
                                      type=openapi.TYPE_STRING, required=True,
                                      description='Телеграмм ID')


class APIPersonInfoByTelegramID(APIView):
    @swagger_auto_schema(
        tags=["person"],
        operation_description='Получает информацию о пользователе по Telegram ID ',
        manual_parameters=[TELEGRAM_ID_QUERY],
    )
    def get(self, request):
        params = request.query_params
        telegram_id = params.get('TelegramId')
        if telegram_id:
            telegram_user = Person.objects.filter(telegram_id=str(telegram_id)).last()
            if telegram_user:
                user_id = telegram_user.pk

                user_photo = None
                if telegram_user.background_image:
                    user_photo = telegram_user.background_image.url

                fio = telegram_user.person_fio
                if not fio:
                    fio = telegram_user.name

                result_dict = {
                    'person_id': user_id,
                    'person_photo': user_photo,
                    'telegram_username': telegram_user.telegram_username,
                    'person_fio': fio,
                    'phone_number': telegram_user.phone_number,
                    'person_date_of_birth': telegram_user.date_of_birth,
                    'email': telegram_user.email,
                }

                return Response({'data': result_dict}, status=200)
            return Response({'error': 'User not found'}, status=400)
        return Response({'error': 'Telegram user not found'}, status=400)

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

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
