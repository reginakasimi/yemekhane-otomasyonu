import pymysql

from web import db
from web.hatalar import IsKuraliHatasi


def bakiye_yukle(kullanici_id, tutar):
    
    baglanti = db.yazma()
    try:
        with baglanti.cursor() as imlec:
            imlec.execute('CALL sp_bakiye_yukle(%s, %s)', (kullanici_id, tutar))
            sonuc = imlec.fetchone()
            while imlec.nextset():
                pass
            return sonuc
    except pymysql.MySQLError as hata:
        if hata.args and hata.args[0] == 1644:
            raise IsKuraliHatasi(hata.args[1])
        raise
    finally:
        baglanti.close()


def hareketler(kullanici_id, kaynaktan=False):
    
    baglanti = db.yazma() if kaynaktan else db.okuma()
    try:
        with baglanti.cursor() as imlec:
            imlec.execute(
                'SELECT id, tur, tutar, aciklama, olusturma '
                'FROM bakiye_hareketleri WHERE kullanici_id = %s '
                'ORDER BY olusturma DESC, id DESC LIMIT 100',
                (kullanici_id,))
            return imlec.fetchall()
    finally:
        baglanti.close()