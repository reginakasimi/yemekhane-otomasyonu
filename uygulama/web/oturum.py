import json
import secrets

from web.redis_baglanti import redis_istemci

OTURUM_SURESI = 30 * 60  
COOKIE_ADI = 'oturum'


def _anahtar(token):
    return f'oturum:{token}'


def olustur(kullanici):
    
    token = secrets.token_urlsafe(32)
    veri = {'id': kullanici['id'], 'ad': kullanici['ad'],
            'soyad': kullanici['soyad'], 'rol': kullanici['rol']}
    redis_istemci().setex(_anahtar(token), OTURUM_SURESI, json.dumps(veri))
    return token


def getir(token):
    
    if not token:
        return None
    r = redis_istemci()
    ham = r.get(_anahtar(token))
    if ham is None:
        return None
    r.expire(_anahtar(token), OTURUM_SURESI)
    return json.loads(ham)


def sil(token):
    if token:
        redis_istemci().delete(_anahtar(token))