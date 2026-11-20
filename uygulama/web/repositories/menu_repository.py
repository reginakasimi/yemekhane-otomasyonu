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



def menu_detay_onbellekli(yemekhane_id, ogun_id, tarih):
    
    import logging
    from web import menu_cache
    log = logging.getLogger(__name__)

    kayit = menu_cache.getir(yemekhane_id, tarih, ogun_id)
    if kayit is not None:
        log.info('MENÜ ÖNBELLEK: İSABET, Redis\'ten okundu (menu:%s:%s:%s)', yemekhane_id, tarih, ogun_id)
        return kayit

    log.info('MENÜ ÖNBELLEK: ISKA, veritabanından okundu (menu:%s:%s:%s)', yemekhane_id, tarih, ogun_id)
    satirlar = menu_detay(yemekhane_id, ogun_id, tarih)
    if satirlar:  
        menu_cache.kaydet(yemekhane_id, tarih, ogun_id, satirlar)
    return satirlar