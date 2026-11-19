from django.urls import path

from web.controllers import auth_controller, saglik_controller

urlpatterns = [
    path('', auth_controller.anasayfa, name='anasayfa'),
    path('giris', auth_controller.giris, name='giris'),
    path('cikis', auth_controller.cikis, name='cikis'),
    path('saglik', saglik_controller.saglik, name='saglik'),
]