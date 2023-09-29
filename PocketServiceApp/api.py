import json
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.views import APIView
from django.http import QueryDict
from celery.result import AsyncResult
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import *
from .serializers import *
from .telegram_tasks import *
from PocketServiceTelegramBot import TOKEN


TELEGRAM_ID_QUERY = openapi.Parameter('TelegramId', in_=openapi.IN_QUERY,
                                      type=openapi.TYPE_STRING, required=True,
                                      description='Телеграмм ID')
CLIENT_ID = openapi.Parameter('ClientId', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, required=True,
                              description='Телеграмм ID клиента')
CLIENT_FIO = openapi.Parameter('ClientFIO', in_=openapi.IN_QUERY,
                                 type=openapi.TYPE_STRING, required=True,
                                 description='ФИО клиента')
CLIENT_PHONE = openapi.Parameter('ClientPhone', in_=openapi.IN_QUERY,
                                 type=openapi.TYPE_STRING, required=True,
                                 description='Телефон клиента')
CLIENT_EMAIL = openapi.Parameter('ClientEmail', in_=openapi.IN_QUERY,
                                 type=openapi.TYPE_STRING, required=True,
                                 description='Email клиента')
CLIENT_ADDRESS = openapi.Parameter('ClientAddress', in_=openapi.IN_QUERY,
                                   type=openapi.TYPE_STRING, required=True,
                                   description='Адрес клиента')
CLIENT_ADDITIONAL_INFO = openapi.Parameter('ClientInfo', in_=openapi.IN_QUERY,
                                           type=openapi.TYPE_STRING, required=True,
                                           description='Дополнительная информация клиента')
AGENT_ID = openapi.Parameter('AgentId', in_=openapi.IN_QUERY,
                             type=openapi.TYPE_STRING, required=True,
                             description='ID агента')
AGENT_TELEGRAM_ID = openapi.Parameter('AgentTelegramId', in_=openapi.IN_QUERY,
                             type=openapi.TYPE_STRING, required=True,
                             description='Телеграмм ID агента')
PRODUCT_ID = openapi.Parameter('ProductId', in_=openapi.IN_QUERY,
                               type=openapi.TYPE_STRING, required=True,
                               description='ID услуги')
PRODUCT_INFO = openapi.Parameter('ProductInfo', in_=openapi.IN_QUERY,
                               type=openapi.TYPE_STRING, required=True,
                               description='Информация об услуге')
ORDER_NAME = openapi.Parameter('OrderName', in_=openapi.IN_QUERY,
                               type=openapi.TYPE_STRING, required=True,
                               description='Имя заявки')
ORDER_PRICE = openapi.Parameter('OrderPrice', in_=openapi.IN_QUERY,
                                type=openapi.TYPE_STRING, required=True,
                                description='Цена заявки')
ORDER_START = openapi.Parameter('OrderStart', in_=openapi.IN_QUERY,
                                type=openapi.TYPE_STRING, required=True,
                                description='Время начала работ')
ORDER_END = openapi.Parameter('OrderEnd', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, required=True,
                              description='Время конца работа')
ORDER_ADDITIONAL_INFO = openapi.Parameter('OrderInfo', in_=openapi.IN_QUERY,
                                          type=openapi.TYPE_STRING, required=True,
                                          description='Дополнительная информация заявки')

status_dict = {
    0: 'Не в работе',
    1: 'В работе',
    2: 'Приостановлена',
    3: 'Выполнена',
}

PRODUCT_TYPES = {
    0: 'Ремонт квартиры',
    1: 'Ремонт сантехники',
    2: 'Ремонт мебели',
    3: 'Уборка',
    4: 'Услуги красоты',
}


def tg_reminder(telegram_id, message, time=0):
    task = tg_message_task.apply_async(kwargs={'telegram_id': telegram_id, 'message': message, 'token': TOKEN},
                                       countdown=time)
    print('TASK CREATES - tg reminder done', task.task_id)
    return task.task_id


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

class APIClientInfoByTelegramID(APIView):
    @swagger_auto_schema(
        tags=["client"],
        operation_description='Получает информацию о клиенте по Telegram ID ',
        manual_parameters=[TELEGRAM_ID_QUERY],
    )
    def get(self, request):
        params = request.query_params
        telegram_id = params.get('TelegramId')
        if telegram_id:
            client = Client.objects.filter(telegram_id=str(telegram_id)).last()
            if client:
                user_id = client.pk

                user_photo = None
                if client.background_image:
                    user_photo = client.background_image.url

                fio = client.person_fio
                if not fio:
                    fio = client.name

                result_dict = {
                    'person_id': user_id,
                    'person_photo': user_photo,
                    'telegram_username': client.telegram_username,
                    'person_fio': fio,
                    'phone_number': client.phone_number,
                    'person_date_of_birth': client.date_of_birth,
                    'email': client.email,
                    'client_address': client.address,
                    'addition_information': client.addition_information,
                }

                return Response({'data': result_dict}, status=200)
            return Response({'error': 'Client not found'}, status=400)
        return Response({'error': 'Telegram user not found'}, status=400)

class APIAgentInfoByTelegramID(APIView):
    @swagger_auto_schema(
        tags=["agent"],
        operation_description='Получает информацию о клиенте по Telegram ID ',
        manual_parameters=[TELEGRAM_ID_QUERY],
    )
    def get(self, request):
        params = request.query_params
        telegram_id = params.get('TelegramId')
        if telegram_id:
            agent = Agent.objects.filter(telegram_id=str(telegram_id)).last()
            if agent:
                user_id = agent.pk

                user_photo = None
                if agent.background_image:
                    user_photo = agent.background_image.url

                fio = agent.person_fio
                if not fio:
                    fio = agent.name

                result_dict = {
                    'person_id': user_id,
                    'person_photo': user_photo,
                    'telegram_username': agent.telegram_username,
                    'person_fio': fio,
                    'phone_number': agent.phone_number,
                    'person_date_of_birth': agent.date_of_birth,
                    'email': agent.email,
                    'agent_description': agent.agent_description,
                    'education_description': agent.education_description,
                    'work_experience': agent.work_experience,
                    'command_work': agent.command_work,
                    'passport_check': agent.passport_check,
                    'contract_work': agent.contract_work,
                    'guarantee_period': agent.guarantee_period,
                }

                return Response({'data': result_dict}, status=200)
            return Response({'error': 'Client not found'}, status=400)
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

class APIPOrdersInfoByAgentTelegramID(APIView):
    @swagger_auto_schema(
        tags=["order"],
        operation_description='Получает информацию о заявках по Telegram ID агента',
        manual_parameters=[TELEGRAM_ID_QUERY],
    )
    def get(self, request):
        params = request.query_params
        telegram_id = params.get('TelegramId')
        if telegram_id:
            agent= Agent.objects.filter(telegram_id=str(telegram_id)).last()
            if agent:
                orders = Order.objects.filter(agent_id=agent.id)
                if orders:
                    orders_list = []
                    for order in orders:
                        product = Product.objects.filter(id=order.product_id).last()
                        client = Client.objects.filter(id=order.client_id).last()
                        orders_list.append(
                            {
                                'order_id': order.id,
                                'order_name': order.name,
                                'order_price': order.price,
                                'order_deadline': order.deadline,
                                'order_start_time': order.start_time,
                                'order_end_time': order.end_time,
                                'order_info': order.addition_information,
                                'order_control': order.control_flag,
                                'order_status': order.status_flag,
                                'order_product_type': PRODUCT_TYPES[int(product.product_type)],
                                'order_product_info': product.addition_information,
                                'order_contact_tg': client.telegram_username,

                            }
                        )
                    result_json = json.dumps(orders_list, indent=4, ensure_ascii=False, default=str)

                    return Response({'data': result_json}, status=200)
                return Response({'error': 'Orders not found'}, status=400)
            return Response({'error': 'User not found'}, status=400)
        return Response({'error': 'Telegram user not found'}, status=400)


class APIPOrdersInfoByClientTelegramID(APIView):
    @swagger_auto_schema(
        tags=["order"],
        operation_description='Получает информацию о заявках по Telegram ID клиента',
        manual_parameters=[TELEGRAM_ID_QUERY],
    )
    def get(self, request):
        params = request.query_params
        telegram_id = params.get('TelegramId')
        if telegram_id:
            client = Client.objects.filter(telegram_id=str(telegram_id)).last()
            if client:
                orders = Order.objects.filter(client_id=client.id)
                if orders:
                    orders_list = []
                    for order in orders:
                        product = Product.objects.filter(id=order.product_id).last()
                        agent = Agent.objects.filter(id=order.agent_id).last()
                        orders_list.append(
                            {
                                'order_id': order.id,
                                'order_name': order.name,
                                'order_price': order.price,
                                'order_deadline': order.deadline,
                                'order_start_time': order.start_time,
                                'order_end_time': order.end_time,
                                'order_info': order.addition_information,
                                'order_control': order.control_flag,
                                'order_status': order.status_flag,
                                'order_product_type': PRODUCT_TYPES[int(product.product_type)],
                                'order_product_info': product.addition_information,
                                'order_contact_tg': agent.telegram_username,
                                'order_contact_phone': agent.phone_number,
                            }
                        )
                    result_json = json.dumps(orders_list, indent=4, ensure_ascii=False, default=str)

                    return Response({'data': result_json}, status=200)
                return Response({'error': 'Orders not found'}, status=400)
            return Response({'error': 'User not found'}, status=400)
        return Response({'error': 'Telegram user not found'}, status=400)


class APIPOrdersCreateByClient(APIView):
    @swagger_auto_schema(
        tags=["order"],
        operation_description='Создание заявки клиента',
        manual_parameters=[CLIENT_ID,
                           CLIENT_PHONE,
                           CLIENT_FIO,
                           CLIENT_EMAIL,
                           CLIENT_ADDRESS,
                           AGENT_TELEGRAM_ID,
                           PRODUCT_ID,
                           PRODUCT_INFO,
                           ORDER_NAME,
                           ORDER_PRICE,
                           ORDER_START,
                           ORDER_END,
                           ORDER_ADDITIONAL_INFO,
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['JSON'],
            properties={
                'JSON': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
    )
    def post(self, request):
        data = request.data
        print(data)
        client_id = data.get('ClientId')
        agent_id = data.get('AgentTelegramId')
        product_info = data.get('ProductInfo')
        client_phone = data.get('ClientPhone')
        client_email = data.get('ClientEmail')

        order_task = create_product_order_task.delay(client_phone, client_id, client_id, data.get('ClientFIO'),
                                                     client_email, data.get('ClientAddress'), data.get('ClientInfo'),
                                                     agent_id, data.get('ProductId'), data.get('OrderName'),
                                                     data.get('OrderPrice'), data.get('OrderStart'),
                                                     data.get('OrderEnd'), data.get('OrderInfo'))
        print('TASK CREATES - create order ', order_task.task_id)

        client_remind_task = tg_reminder(client_id, "Вы зарегистрировали заявку на <b>{}</b>. \n"
                                                    "Ожидайте, как с вами свяжется исполнитель!"
                                         .format(product_info))
        print('TASK CREATES - client remind ', client_remind_task)

        agent_remind_task = tg_reminder(agent_id, "Вам пришла заявка на <b>{}</b>.\n"
                                                  "Свяжитесь с заказчиком. \n"
                                                  "Телефон: <b>{}</b> \n"
                                                  "Электронная почта: <b>{}</b>"
                                        .format(product_info, client_phone, client_email))
        print('TASK CREATES - agent remind ', agent_remind_task)

        agent_remind_task = tg_reminder(agent_id, "Напоминанем, что вам пришла заявка на <b>{}</b>.\n"
                                                  "Свяжитесь с заказчиком и отметьте в личном "
                                                  "кабинете информацию о принятии заказа. \n"
                                                  "Телефон: <b>{}</b> \n"
                                                  "Электронная почта: <b>{}</b>"
                                        .format(product_info, client_phone, client_email),
                                        time=10)
        print('TASK CREATES - agent remind 3h ', agent_remind_task)

        update_order_task = update_product_order_task.delay(order_id=order_task.get(), reminder_status=1)
        print('TASK CREATES - update order', update_order_task.task_id)

        return Response({'Result': 'Order Created'}, status=200)


class APIPPricesInfoByAgentID(APIView):
    @swagger_auto_schema(
        tags=["price"],
        operation_description='Получает информацию о ценах на услуги агента по его ID',
        manual_parameters=[AGENT_ID],
    )
    def get(self, request):
        params = request.query_params
        agent_id = params.get('AgentId')
        if agent_id:
            agent = Agent.objects.filter(id=str(agent_id)).last()
            if agent:
                prices = Price.objects.filter(agent_id=agent_id)
                if prices:
                    product_prices = {}
                    for price in prices:
                        product = Product.objects.filter(id=price.product_id).last()
                        product_type = PRODUCT_TYPES[int(product.product_type)]
                        if product_type not in product_prices.keys():
                            product_prices[product_type] = {}
                        product_prices[product_type][product.addition_information] = [price.price_value, price.product_id]

                    result_json = json.dumps(product_prices, indent=4, ensure_ascii=False, default=str)

                    return Response({'data': result_json}, status=200)
                return Response({'error': 'Prices not found'}, status=400)
            return Response({'error': 'Agent not found'}, status=400)
        return Response({'error': 'Agent ID not found'}, status=400)

class APIPEducationsInfoByAgentID(APIView):
    @swagger_auto_schema(
        tags=["education"],
        operation_description='Получает информацию об образовании агента по его ID',
        manual_parameters=[AGENT_ID],
    )
    def get(self, request):
        params = request.query_params
        agent_id = params.get('AgentId')
        if agent_id:
            agent = Agent.objects.filter(id=str(agent_id)).last()
            if agent:
                educations = Education.objects.filter(agent_id=agent_id)
                if educations:
                    educations_info = []
                    for education in educations:
                        specialization = Specialization.objects.filter(id=education.specialization_id).last().name
                        university = University.objects.filter(id=education.university_id).last().name
                        educations_info.append({
                            'specialization': specialization,
                            'university': university,
                            'education_start': education.period_start,
                            'education_end': education.period_end,
                            'education_checked': education.document_check,
                        })
                    result_json = json.dumps(educations_info, indent=4, ensure_ascii=False, default=str)

                    return Response({'data': result_json}, status=200)
                return Response({'error': 'Educations not found'}, status=400)
            return Response({'error': 'Agent not found'}, status=400)
        return Response({'error': 'Agent ID not found'}, status=400)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class AdminsViewSet(viewsets.ModelViewSet):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


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
