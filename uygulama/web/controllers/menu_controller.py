import datetime

from django.shortcuts import render

from web.decorators import giris_gerekli
from web.repositories import kullanici_repository, menu_repository


def _sayi(deger, varsayilan):
    try:
        return int(deger)
    except (TypeError, ValueError):
        return varsayilan


def _tarih(deger):
    try:
        return datetime.date.fromisoformat(deger)
    except (TypeError, ValueError):
        return datetime.date.today()


@giris_gerekli
def gunun_menusu(request):
    yemekhane_listesi = menu_repository.yemekhaneler()
    ogun_listesi = menu_repository.ogunler()

    
    yemekhane_id = _sayi(request.GET.get('yemekhane'), 1)
    ogun_id = _sayi(request.GET.get('ogun'), 2)
    tarih = _tarih(request.GET.get('tarih'))

    satirlar = menu_repository.menu_detay_onbellekli(yemekhane_id, ogun_id, tarih)

    toplam_kalori = sum(s['kalori'] or 0 for s in satirlar)

   
    kategoriler = []
    for s in satirlar:
        if not kategoriler or kategoriler[-1]['ad'] != s['kategori']:
            kategoriler.append({'ad': s['kategori'], 'yemekler': []})
        kategoriler[-1]['yemekler'].append(s)

    ust = satirlar[0] if satirlar else None
    fiyat = None
    if ust:
       
        fiyat = ust['ogrenci_fiyati'] if request.kullanici['rol'] == 'ogrenci' else ust['personel_fiyati']

    baglam = {
        'kullanici': request.kullanici,
        'bakiye': kullanici_repository.bakiye_getir(request.kullanici['id']),
        'yemekhaneler': yemekhane_listesi,
        'ogunler': ogun_listesi,
        'secili_yemekhane': yemekhane_id,
        'secili_ogun': ogun_id,
        'tarih': tarih.isoformat(),
        'kategoriler': kategoriler,
        'ust': ust,
        'fiyat': fiyat,
        'toplam_kalori': toplam_kalori,
    }
    return render(request, 'web/gunun_menusu.html', baglam)