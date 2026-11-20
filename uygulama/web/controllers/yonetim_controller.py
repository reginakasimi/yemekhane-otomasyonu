import datetime
import logging
from decimal import Decimal, InvalidOperation

from web import menu_cache

from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from web.decorators import giris_gerekli
from web.hatalar import IsKuraliHatasi
from web.repositories import kullanici_repository, menu_repository, yonetim_repository

log = logging.getLogger(__name__)


def _sayi(deger, varsayilan):
    try:
        return int(deger)
    except (TypeError, ValueError):
        return varsayilan


def _para(deger):
    try:
        d = Decimal(str(deger).strip().replace(',', '.'))
    except InvalidOperation:
        return None
    return d if d >= 0 else None


def yonetici_gerekli(gorunum):
    """Только роль yonetici. Остальным 403."""
    @giris_gerekli
    def sarmalayici(request, *args, **kwargs):
        if request.kullanici['rol'] != 'yonetici':
            return HttpResponseForbidden('Bu sayfaya erişim yetkiniz yok.')
        return gorunum(request, *args, **kwargs)
    sarmalayici.__name__ = gorunum.__name__
    return sarmalayici


@yonetici_gerekli
def yonetim(request):
    baglam = {
        'kullanici': request.kullanici,
        'bakiye': kullanici_repository.bakiye_getir(request.kullanici['id']),
        'menuler': yonetim_repository.menu_listesi(),
        'basari': request.GET.get('ok'),
    }
    return render(request, 'web/yonetim.html', baglam)


@yonetici_gerekli
def menu_form(request, menu_id=None):
    duzenleme = menu_id is not None
    mevcut = yonetim_repository.menu_getir(menu_id) if duzenleme else None
    if duzenleme and mevcut is None:
        return redirect('/yonetim')

    hata = None
    if request.method == 'POST':
        ogrenci = _para(request.POST.get('ogrenci_fiyati'))
        personel = _para(request.POST.get('personel_fiyati'))
        yemekler = [_sayi(v, 0) for v in request.POST.getlist('yemek')]
        if ogrenci is None or personel is None:
            hata = 'Fiyatlar geçerli ve sıfırdan küçük olmayan sayılar olmalıdır.'
        elif not yemekler:
            hata = 'En az bir yemek seçin.'
        else:
            try:
                if duzenleme:
                    yonetim_repository.menu_guncelle(menu_id, ogrenci, personel, yemekler)
                    menu_cache.sil(mevcut['yemekhane_id'], mevcut['tarih'], mevcut['ogun_id'])
                    return redirect('/yonetim?ok=Menü güncellendi.')
                tarih = datetime.date.fromisoformat(request.POST.get('tarih', ''))
                yemekhane_id = _sayi(request.POST.get('yemekhane'), 1)
                ogun_id = _sayi(request.POST.get('ogun'), 1)
                yonetim_repository.menu_olustur(
                    yemekhane_id, tarih, ogun_id, ogrenci, personel, yemekler)
                menu_cache.sil(yemekhane_id, tarih, ogun_id)
                return redirect('/yonetim?ok=Menü oluşturuldu.')
            except ValueError:
                hata = 'Geçerli bir tarih girin.'
            except IsKuraliHatasi as e:
                hata = str(e)
            except Exception:
                log.exception('Menü kaydetme hatası')
                hata = 'Beklenmeyen bir hata oluştu.'

    baglam = {
        'kullanici': request.kullanici,
        'bakiye': kullanici_repository.bakiye_getir(request.kullanici['id']),
        'duzenleme': duzenleme,
        'menu': mevcut,
        'yemekhaneler': menu_repository.yemekhaneler(),
        'ogunler': menu_repository.ogunler(),
        'yemekler': yonetim_repository.tum_yemekler(),
        'hata': hata,
    }
    return render(request, 'web/menu_form.html', baglam)