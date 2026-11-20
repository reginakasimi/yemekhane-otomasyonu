import logging

from django.shortcuts import render

from web.decorators import giris_gerekli
from web.hatalar import IsKuraliHatasi
from web.repositories import degerlendirme_repository, kullanici_repository

log = logging.getLogger(__name__)


def _sayi(deger, varsayilan):
    try:
        return int(deger)
    except (TypeError, ValueError):
        return varsayilan


@giris_gerekli
def degerlendirme(request):
    kullanici = request.kullanici
    basari, hata = None, None

    if request.method == 'POST':
        puan = _sayi(request.POST.get('puan'), 0)
        yorum = request.POST.get('yorum', '').strip()[:500]
        if puan < 1 or puan > 5:
            hata = 'Puan 1 ile 5 arasında olmalıdır.'
        else:
            try:
                degerlendirme_repository.degerlendir(
                    kullanici['id'], _sayi(request.POST.get('menu_id'), 0), puan, yorum)
                basari = 'Değerlendirmeniz kaydedildi. Teşekkürler!'
            except IsKuraliHatasi as e:
                hata = str(e)
            except Exception:
                log.exception('Değerlendirme hatası')
                hata = 'Beklenmeyen bir hata oluştu.'

    baglam = {
        'kullanici': kullanici,
        'bakiye': kullanici_repository.bakiye_getir(kullanici['id']),
        'menuler': degerlendirme_repository.kullanilmis_menuler(kullanici['id']),
        'basari': basari,
        'hata': hata,
    }
    return render(request, 'web/degerlendirme.html', baglam)