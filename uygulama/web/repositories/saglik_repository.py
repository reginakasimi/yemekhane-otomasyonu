from web import db


def _sunucu_bilgisi(baglanti_fonksiyonu):
    baglanti = baglanti_fonksiyonu()
    try:
        with baglanti.cursor() as imlec:
            imlec.execute('SELECT @@hostname AS sunucu, @@super_read_only AS salt_okunur')
            return imlec.fetchone()
    finally:
        baglanti.close()


def yazma_sunucusu():
    return _sunucu_bilgisi(db.yazma)


def okuma_sunucusu():
    return _sunucu_bilgisi(db.okuma)