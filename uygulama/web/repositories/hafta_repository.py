from web import db


def hafta_menuleri(yemekhane_id, baslangic, bitis):
    baglanti = db.okuma()
    try:
        with baglanti.cursor() as imlec:
            imlec.execute(
                'SELECT m.id AS menu_id, m.tarih, o.ad AS ogun, o.sira AS ogun_sira, '
                'd.kapasite, d.bos_yer, m.ogrenci_fiyati, m.personel_fiyati, '
                'COALESCE(d.rezervasyon_son < NOW(), 0) AS suresi_doldu '
                'FROM menuler m '
                'JOIN ogunler o ON o.id = m.ogun_id '
                'JOIN v_menu_doluluk d ON d.menu_id = m.id '
                'WHERE m.yemekhane_id = %s AND m.tarih BETWEEN %s AND %s '
                'ORDER BY m.tarih, o.sira',
                (yemekhane_id, baslangic, bitis))
            return imlec.fetchall()
    finally:
        baglanti.close()