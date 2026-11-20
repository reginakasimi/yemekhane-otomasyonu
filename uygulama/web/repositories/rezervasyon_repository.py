import pymysql

from web import db
from web.hatalar import IsKuraliHatasi


def rezervasyon_yap(kullanici_id, menu_id):
    
    baglanti = db.yazma()
    try:
        with baglanti.cursor() as imlec:
            imlec.execute('CALL sp_rezervasyon_yap(%s, %s)', (kullanici_id, menu_id))
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