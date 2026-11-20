from django.urls import path

from web.controllers import (auth_controller, bakiye_controller, degerlendirme_controller,
                             menu_controller, rezervasyon_controller, saglik_controller,
                             yonetim_controller)

urlpatterns = [
    path('', auth_controller.anasayfa, name='anasayfa'),
    path('giris', auth_controller.giris, name='giris'),
    path('cikis', auth_controller.cikis, name='cikis'),
    path('menu', menu_controller.gunun_menusu, name='menu'),
    path('hafta', rezervasyon_controller.haftalik, name='hafta'),
    path('rezervasyonlarim', rezervasyon_controller.rezervasyonlarim, name='rezervasyonlarim'),
    path('bakiye', bakiye_controller.bakiye, name='bakiye'),
    path('degerlendirme', degerlendirme_controller.degerlendirme, name='degerlendirme'),
    path('yonetim', yonetim_controller.yonetim, name='yonetim'),
    path('yonetim/yeni', yonetim_controller.menu_form, name='menu_yeni'),
    path('yonetim/duzenle/<int:menu_id>', yonetim_controller.menu_form, name='menu_duzenle'),
    path('saglik', saglik_controller.saglik, name='saglik'),
]