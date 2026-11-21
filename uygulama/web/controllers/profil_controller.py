import logging

from django.shortcuts import render

from web.decorators import giris_gerekli
from web.repositories import kullanici_repository, profil_repository

log = logging.getLogger(__name__)


@giris_gerekli
def profil(request):
    kullanici = request.kullanici
    alerjenler = profil_repository.tum_alerjenler()
    gecerli = {a['id'] for a in alerjenler}
    basari, hata = None, None

    if request.method == 'POST':
        secilen = set()
        for v in request.POST.getlist('alerjen'):
            if v.isdigit() and int(v) in gecerli:
                secilen.add(int(v))
        try:
            profil_repository.alerjenleri_kaydet(kullanici['id'], secilen)
            basari = 'Alerjen tercihleriniz kaydedildi.'
        except Exception:
            log.exception('Alerjen kaydetme hatası')
            hata = 'Beklenmeyen bir hata oluştu.'

    secili = profil_repository.secili_alerjen_idleri(kullanici['id'])
    baglam = {
        'kullanici': kullanici,
        'bakiye': kullanici_repository.bakiye_getir(kullanici['id']),
        'alerjenler': [{'id': a['id'], 'ad': a['ad'], 'secili': a['id'] in secili} for a in alerjenler],
        'basari': basari,
        'hata': hata,
    }
    return render(request, 'web/profil.html', baglam)