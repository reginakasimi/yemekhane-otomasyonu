from web import db


def _sorgu(sql, parametreler=()):
    baglanti = db.okuma()
    try:
        with baglanti.cursor() as imlec:
            imlec.execute(sql, parametreler)
            return imlec.fetchall()
    finally:
        baglanti.close()


def yemekhaneler():
    return _sorgu('SELECT id, ad FROM yemekhaneler ORDER BY id')


def ogunler():
    return _sorgu('SELECT id, ad, son_saat FROM ogunler ORDER BY sira')


def menu_detay(yemekhane_id, ogun_id, tarih):
    
    return _sorgu(
        'SELECT menu_id, yemekhane, ogun, rezervasyon_son, '
        'ogrenci_fiyati, personel_fiyati, yemek, kategori, kategori_sira, '
        'kalori, vejetaryen, alerjenler '
        'FROM v_menu_detay '
        'WHERE yemekhane_id = %s AND ogun_id = %s AND tarih = %s '
        'ORDER BY kategori_sira, yemek',
        (yemekhane_id, ogun_id, tarih))