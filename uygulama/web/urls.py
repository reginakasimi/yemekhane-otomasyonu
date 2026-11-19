from django.urls import path

from web.controllers import saglik_controller

urlpatterns = [
    path('saglik', saglik_controller.saglik, name='saglik'),
]