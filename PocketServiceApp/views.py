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


