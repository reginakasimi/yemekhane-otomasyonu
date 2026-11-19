import bcrypt
from django.shortcuts import redirect, render

from web import oturum
from web.decorators import giris_gerekli
from web.repositories import kullanici_repository


def giris(request):
    
    if oturum.getir(request.COOKIES.get(oturum.COOKIE_ADI)):
        return redirect('/')

    hata = None
    if request.method == 'POST':
        eposta = request.POST.get('eposta', '').strip()
        sifre = request.POST.get('sifre', '')
        kullanici = kullanici_repository.eposta_ile_bul(eposta)

        dogru = (
            kullanici is not None
            and kullanici['aktif']
            and bcrypt.checkpw(sifre.encode('utf-8'), kullanici['sifre_hash'].encode('utf-8'))
        )
        if dogru:
            token = oturum.olustur(kullanici)
            cevap = redirect('/')
            cevap.set_cookie(oturum.COOKIE_ADI, token, max_age=oturum.OTURUM_SURESI,
                             httponly=True, samesite='Lax')
            return cevap
        hata = 'E-posta veya şifre hatalı.'

    return render(request, 'web/giris.html', {'hata': hata})


@giris_gerekli
def cikis(request):
    oturum.sil(request.oturum_token)
    cevap = redirect('/giris')
    cevap.delete_cookie(oturum.COOKIE_ADI)
    return cevap


@giris_gerekli
def anasayfa(request):
    bakiye = kullanici_repository.bakiye_getir(request.kullanici['id'])
    return render(request, 'web/anasayfa.html',
                  {'kullanici': request.kullanici, 'bakiye': bakiye})