from django.urls import path

from PocketServiceApp import consumers


urlpatterns = [
    path('ws/task_status/', consumers.ClientStatusConsumer.as_asgi()),
]