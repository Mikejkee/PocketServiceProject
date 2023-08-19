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

class APICompanyInfoByTelegramID(APIView):
    @swagger_auto_schema(
        tags=["company"],
        operation_description='Получает информацию о компании по Telegram ID управляющего ',
        manual_parameters=[TELEGRAM_ID_QUERY],
    )
    def get(self, request):
        params = request.query_params
        telegram_id = params.get('TelegramId')
        if telegram_id:
            agent = Agent.objects.filter(telegram_id=str(telegram_id)).last()
            if agent:
                roles = agent.role
                if roles.filter(role_type='Управляющий организации').last():
                    company_id = agent.company_id
                    company = Company.objects.filter(id=str(company_id)).last()
                    if company:
                        result_dict = {
                            'company_id': company_id,
                            'company_name': company.name,
                            'company_description': company.description,
                            'company_legal_address': company.legal_address,
                            'company_mail_address': company.mail_address,
                            'company_inn': company.inn,
                            'company_kpp': company.kpp,
                            'company_ogrnip': company.ogrnip,
                            'company_payment_account': company.payment_account,
                            'company_bank': company.bank,
                            'company_bik': company.bik,
                            'company_okpo': company.okpo,
                            'company_contact_phone': company.contact_phone,
                            'company_email': company.email,
                        }

                        return Response({'data': result_dict}, status=200)
                    return Response({'error': 'Company is not found'}, status=400)
                return Response({'error': 'User is not head of company'}, status=400)
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


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

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
