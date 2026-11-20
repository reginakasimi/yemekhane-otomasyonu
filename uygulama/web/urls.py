from django.urls import path

from web.controllers import (auth_controller, menu_controller,
                             rezervasyon_controller, saglik_controller)

urlpatterns = [
    path('', auth_controller.anasayfa, name='anasayfa'),
    path('giris', auth_controller.giris, name='giris'),
    path('cikis', auth_controller.cikis, name='cikis'),
    path('menu', menu_controller.gunun_menusu, name='menu'),
    path('hafta', rezervasyon_controller.haftalik, name='hafta'),
    path('saglik', saglik_controller.saglik, name='saglik'),
]