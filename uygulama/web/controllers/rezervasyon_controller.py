import datetime
import logging
from decimal import ROUND_HALF_UP, Decimal

from django.shortcuts import render

from web.decorators import giris_gerekli
from web.hatalar import IsKuraliHatasi
from web.repositories import (hafta_repository, kullanici_repository,
                              menu_repository, rezervasyon_repository)

log = logging.getLogger(__name__)
GUNLER = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']


def _tarih(deger):
    try:
        return datetime.date.fromisoformat(deger)
    except (TypeError, ValueError):
        return datetime.date.today()


def _sayi(deger, varsayilan):
    try:
        return int(deger)
    except (TypeError, ValueError):
        return varsayilan


@giris_gerekli
def haftalik(request):
    kullanici = request.kullanici
    veri = request.POST if request.method == 'POST' else request.GET
    yemekhane_id = _sayi(veri.get('yemekhane'), 1)
    pazartesi = _tarih(veri.get('hafta'))
    pazartesi -= datetime.timedelta(days=pazartesi.weekday())

    basari, hata = None, None
    if request.method == 'POST':
        try:
            sonuc = rezervasyon_repository.rezervasyon_yap(
                kullanici['id'], _sayi(veri.get('menu_id'), 0),
                veri.get('porsiyon', 'tam'))
            basari = f"Rezervasyon yapıldı. Ücret: {sonuc['ucret']} TL, yeni bakiye: {sonuc['bakiye']} TL."
        except IsKuraliHatasi as e:
            hata = str(e) 
        except Exception:
            log.exception('Rezervasyon hatası')
            hata = 'Beklenmeyen bir hata oluştu.'

    pazar = pazartesi + datetime.timedelta(days=6)
    satirlar = hafta_repository.hafta_menuleri(yemekhane_id, pazartesi, pazar)
    benim = rezervasyon_repository.aktif_menuler(kullanici['id'], [s['menu_id'] for s in satirlar])

    gunler = {}
    for s in satirlar:
        s['fiyat'] = s['ogrenci_fiyati'] if kullanici['rol'] == 'ogrenci' else s['personel_fiyati']
        s['yarim_var'] = s['ogun_sira'] != 1 
        s['yarim_fiyat'] = (s['fiyat'] * Decimal('0.60')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if s['menu_id'] in benim:
            s['durum'] = 'rezerve'
        elif s['suresi_doldu']:
            s['durum'] = 'suresi_doldu'
        elif s['bos_yer'] <= 0:
            s['durum'] = 'dolu'
        else:
            s['durum'] = 'acik'
        gunler.setdefault(s['tarih'], []).append(s)

    gun_listesi = [
        {'tarih': t, 'ad': GUNLER[t.weekday()], 'ogunler': liste}
        for t, liste in gunler.items()
    ]

    baglam = {
        'kullanici': kullanici,
        'bakiye': kullanici_repository.bakiye_getir(kullanici['id']),  
        'yemekhaneler': menu_repository.yemekhaneler(),
        'secili_yemekhane': yemekhane_id,
        'hafta': pazartesi.isoformat(),
        'onceki': (pazartesi - datetime.timedelta(days=7)).isoformat(),
        'sonraki': (pazartesi + datetime.timedelta(days=7)).isoformat(),
        'gunler': gun_listesi,
        'basari': basari,
        'hata': hata,
    }
    return render(request, 'web/haftalik.html', baglam)




@giris_gerekli
def rezervasyonlarim(request):
    kullanici = request.kullanici
    basari, hata = None, None

    if request.method == 'POST':
        try:
            sonuc = rezervasyon_repository.iptal_et(
                kullanici['id'], _sayi(request.POST.get('rezervasyon_id'), 0))
            basari = f"Rezervasyon iptal edildi. İade: {sonuc['iade']} TL, yeni bakiye: {sonuc['bakiye']} TL."
        except IsKuraliHatasi as e:
            hata = str(e)
        except Exception:
            log.exception('İptal hatası')
            hata = 'Beklenmeyen bir hata oluştu.'

    baglam = {
        'kullanici': kullanici,
        'bakiye': kullanici_repository.bakiye_getir(kullanici['id']),
        'rezervasyonlar': rezervasyon_repository.kullanici_rezervasyonlari(kullanici['id']),
        'basari': basari,
        'hata': hata,
    }
    return render(request, 'web/rezervasyonlarim.html', baglam)