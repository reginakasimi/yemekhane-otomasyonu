from web import db


def eposta_ile_bul(eposta):
   
    baglanti = db.okuma()
    try:
        with baglanti.cursor() as imlec:
            imlec.execute(
                'SELECT id, ad, soyad, eposta, sifre_hash, rol, aktif '
                'FROM kullanicilar WHERE eposta = %s', (eposta,))
            return imlec.fetchone()
    finally:
        baglanti.close()


def bakiye_getir(kullanici_id):
    
    baglanti = db.yazma()
    try:
        with baglanti.cursor() as imlec:
            imlec.execute('SELECT bakiye FROM kullanicilar WHERE id = %s', (kullanici_id,))
            satir = imlec.fetchone()
            return satir['bakiye'] if satir else None
    finally:
        baglanti.close()