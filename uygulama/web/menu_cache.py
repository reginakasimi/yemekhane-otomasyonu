import datetime
import json
import logging

from web.redis_baglanti import redis_istemci

log = logging.getLogger(__name__)


def anahtar(yemekhane_id, tarih, ogun_id):
    return f'menu:{yemekhane_id}:{tarih}:{ogun_id}'


def getir(yemekhane_id, tarih, ogun_id):
    ham = redis_istemci().get(anahtar(yemekhane_id, tarih, ogun_id))
    return json.loads(ham) if ham is not None else None


def kaydet(yemekhane_id, tarih, ogun_id, satirlar):
   
    gun_sonu = datetime.datetime.combine(tarih, datetime.time(23, 59, 59))
    sure = max(int((gun_sonu - datetime.datetime.now()).total_seconds()), 60)
    redis_istemci().setex(anahtar(yemekhane_id, tarih, ogun_id), sure,
                          json.dumps(satirlar, default=str))


def sil(yemekhane_id, tarih, ogun_id):
    redis_istemci().delete(anahtar(yemekhane_id, tarih, ogun_id))
    log.info('MENÜ ÖNBELLEK: silindi (%s)', anahtar(yemekhane_id, tarih, ogun_id))