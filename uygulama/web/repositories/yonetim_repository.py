import pymysql

from web import db
from web.hatalar import IsKuraliHatasi


def menu_listesi():
    
    baglanti = db.okuma()
    try:
        with baglanti.cursor() as imlec:
            imlec.execute(
                'SELECT d.menu_id, d.tarih, d.yemekhane, d.ogun, d.kapasite, d.rezerve, '
                'd.bos_yer, d.doluluk_yuzde, p.oy_sayisi, p.ortalama_puan '
                'FROM v_menu_doluluk d '
                'LEFT JOIN v_menu_puan p ON p.menu_id = d.menu_id '
                'ORDER BY d.tarih DESC, d.yemekhane, d.ogun_id '
                'LIMIT 100')
            return imlec.fetchall()
    finally:
        baglanti.close()


def tum_yemekler():
    baglanti = db.okuma()
    try:
        with baglanti.cursor() as imlec:
            imlec.execute(
                'SELECT y.id, y.ad, y.kalori, k.ad AS kategori '
                'FROM yemekler y JOIN yemek_kategorileri k ON k.id = y.kategori_id '
                'ORDER BY k.sira, y.ad')
            return imlec.fetchall()
    finally:
        baglanti.close()


def menu_getir(menu_id):
   
    baglanti = db.yazma()
    try:
        with baglanti.cursor() as imlec:
            imlec.execute(
                'SELECT id, yemekhane_id, tarih, ogun_id, ogrenci_fiyati, personel_fiyati '
                'FROM menuler WHERE id = %s', (menu_id,))
            menu = imlec.fetchone()
            if menu is None:
                return None
            imlec.execute('SELECT yemek_id FROM menu_yemekleri WHERE menu_id = %s', (menu_id,))
            menu['yemek_idleri'] = {s['yemek_id'] for s in imlec.fetchall()}
            return menu
    finally:
        baglanti.close()


def _yemekleri_yaz(imlec, menu_id, yemek_idleri):
    imlec.execute('DELETE FROM menu_yemekleri WHERE menu_id = %s', (menu_id,))
    for yid in yemek_idleri:
        imlec.execute('INSERT INTO menu_yemekleri (menu_id, yemek_id) VALUES (%s, %s)',
                      (menu_id, yid))


def menu_olustur(yemekhane_id, tarih, ogun_id, ogrenci_fiyati, personel_fiyati, yemek_idleri):
    baglanti = db.yazma()
    try:
        baglanti.begin()
        with baglanti.cursor() as imlec:
            try:
                imlec.execute(
                    'INSERT INTO menuler (yemekhane_id, tarih, ogun_id, ogrenci_fiyati, personel_fiyati) '
                    'VALUES (%s, %s, %s, %s, %s)',
                    (yemekhane_id, tarih, ogun_id, ogrenci_fiyati, personel_fiyati))
            except pymysql.err.IntegrityError as hata:
                baglanti.rollback()
                if hata.args[0] == 1062:
                    raise IsKuraliHatasi('Bu yemekhane, tarih ve öğün için zaten bir menü var.')
                raise
            menu_id = imlec.lastrowid
            _yemekleri_yaz(imlec, menu_id, yemek_idleri)
        baglanti.commit()
        return menu_id
    except Exception:
        baglanti.rollback()
        raise
    finally:
        baglanti.close()


def menu_guncelle(menu_id, ogrenci_fiyati, personel_fiyati, yemek_idleri):
    baglanti = db.yazma()
    try:
        baglanti.begin()
        with baglanti.cursor() as imlec:
            imlec.execute(
                'UPDATE menuler SET ogrenci_fiyati = %s, personel_fiyati = %s WHERE id = %s',
                (ogrenci_fiyati, personel_fiyati, menu_id))
            _yemekleri_yaz(imlec, menu_id, yemek_idleri)
        baglanti.commit()
    except Exception:
        baglanti.rollback()
        raise
    finally:
        baglanti.close()