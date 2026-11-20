import logging
from decimal import Decimal, InvalidOperation

from django.shortcuts import render

from web.decorators import giris_gerekli
from web.hatalar import IsKuraliHatasi
from web.repositories import bakiye_repository, kullanici_repository

log = logging.getLogger(__name__)


@giris_gerekli
def bakiye(request):
    kullanici = request.kullanici
    basari, hata = None, None
    yukleme_yapildi = False

    if request.method == 'POST':
        ham = request.POST.get('tutar', '').strip().replace(',', '.')
        try:
            tutar = Decimal(ham)
        except InvalidOperation:
            tutar = None
        if tutar is None:
            hata = 'Geçerli bir tutar girin.'
        else:
            try:
                sonuc = bakiye_repository.bakiye_yukle(kullanici['id'], tutar)
                basari = f"Bakiye yüklendi. Yeni bakiye: {sonuc['bakiye']} TL."
                yukleme_yapildi = True
            except IsKuraliHatasi as e:
                hata = str(e)  
            except Exception:
                log.exception('Bakiye yükleme hatası')
                hata = 'Beklenmeyen bir hata oluştu.'

    baglam = {
        'kullanici': kullanici,
        'bakiye': kullanici_repository.bakiye_getir(kullanici['id']),  
        'hareketler': bakiye_repository.hareketler(kullanici['id'], kaynaktan=yukleme_yapildi),
        'basari': basari,
        'hata': hata,
    }
    return render(request, 'web/bakiye.html', baglam)