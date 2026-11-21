import pymysql

from web import db
from web.hatalar import IsKuraliHatasi


def rezervasyon_yap(kullanici_id, menu_id, porsiyon='tam'):
    
    baglanti = db.yazma()
    try:
        with baglanti.cursor() as imlec:
            imlec.execute('CALL sp_rezervasyon_yap(%s, %s, %s)', (kullanici_id, menu_id, porsiyon))
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


def aktif_menuler(kullanici_id, menu_idleri):
    
    if not menu_idleri:
        return set()
    baglanti = db.yazma()
    try:
        with baglanti.cursor() as imlec:
            yer = ','.join(['%s'] * len(menu_idleri))
            imlec.execute(
                'SELECT menu_id FROM rezervasyonlar '
                f"WHERE kullanici_id = %s AND durum = 'aktif' AND menu_id IN ({yer})",
                [kullanici_id, *menu_idleri])
            return {satir['menu_id'] for satir in imlec.fetchall()}
    finally:
        baglanti.close()



def iptal_et(kullanici_id, rezervasyon_id):
    """Вызывает sp_rezervasyon_iptal на источнике. Возвращает {rezervasyon_id, iade, bakiye}."""
    baglanti = db.yazma()
    try:
        with baglanti.cursor() as imlec:
            imlec.execute('CALL sp_rezervasyon_iptal(%s, %s)', (kullanici_id, rezervasyon_id))
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


def kullanici_rezervasyonlari(kullanici_id):
    
    baglanti = db.yazma()
    try:
        with baglanti.cursor() as imlec:
            imlec.execute(
                'SELECT r.id, r.durum, r.ucret, r.olusturma, r.kullanma_zamani, r.iptal_zamani, '
                'm.tarih, y.ad AS yemekhane, o.ad AS ogun, '
                'COALESCE(CONCAT(m.tarih, " ", o.son_saat) > NOW(), 0) AS iptal_edilebilir '
                'FROM rezervasyonlar r '
                'JOIN menuler m ON m.id = r.menu_id '
                'JOIN yemekhaneler y ON y.id = m.yemekhane_id '
                'JOIN ogunler o ON o.id = m.ogun_id '
                'WHERE r.kullanici_id = %s '
                'ORDER BY m.tarih DESC, o.sira',
                (kullanici_id,))
            return imlec.fetchall()
    finally:
        baglanti.close()