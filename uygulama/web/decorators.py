from functools import wraps

from django.shortcuts import redirect

from web import oturum


def giris_gerekli(gorunum):
    @wraps(gorunum)
    def sarmalayici(request, *args, **kwargs):
        token = request.COOKIES.get(oturum.COOKIE_ADI)
        kullanici = oturum.getir(token)
        if kullanici is None:
            return redirect('/giris')
        request.kullanici = kullanici
        request.oturum_token = token
        return gorunum(request, *args, **kwargs)
    return sarmalayici