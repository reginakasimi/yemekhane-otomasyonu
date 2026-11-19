from django.shortcuts import render

from web.repositories import saglik_repository


def saglik(request):
    baglam = {'yazma': None, 'okuma': None, 'hata': None}
    try:
        baglam['yazma'] = saglik_repository.yazma_sunucusu()
        baglam['okuma'] = saglik_repository.okuma_sunucusu()
    except Exception as hata:
        baglam['hata'] = str(hata)
    return render(request, 'web/saglik.html', baglam, status=503 if baglam['hata'] else 200)