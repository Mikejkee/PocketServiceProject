from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound

from .models import *


def delete_all_data_in_data_base():
    Role.objects.all().delete()
    Area.objects.all().delete()
    ImageObject.objects.all().delete()
    FileObject.objects.all().delete()
    Agent.objects.all().delete()
    Client.objects.all().delete()
    Administrator.objects.all().delete()
    Product.objects.all().delete()
    Order.objects.all().delete()

def index(request):
    delete_all_data_in_data_base()
    # new_admin = Administrator.objects.create(name='Имя', surname="Фамилия", patronymic="Отчество", date_of_birth="2022-03-12",
    #                                  phone_number="Номер", username="Имя", telegram_id="ID",
    #                                  telegram_username="Имя ", email="dsdsds@yandex.ru",
    #                                  whom_created='Кто', addition_information="Дополнительная")
    # new_admin.save()
    # new_admin.background_image.create(object_type='Картинка', object_url="Home/")
    # new_admin.background_image.create(object_type='Картинка', object_url="Home/1")
    # new_admin.save()
    # print(new_admin.background_image.all())
    return HttpResponseNotFound()


