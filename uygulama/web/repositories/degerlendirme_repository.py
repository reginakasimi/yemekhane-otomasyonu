import pymysql

from web import db
from web.hatalar import IsKuraliHatasi


def kullanilmis_menuler(kullanici_id):
    
    baglanti = db.yazma()
    try:
        with baglanti.cursor() as imlec:
            imlec.execute(
                'SELECT m.id AS menu_id, m.tarih, y.ad AS yemekhane, o.ad AS ogun, '
                'd.puan, d.yorum '
                'FROM rezervasyonlar r '
                'JOIN menuler m ON m.id = r.menu_id '
                'JOIN yemekhaneler y ON y.id = m.yemekhane_id '
                'JOIN ogunler o ON o.id = m.ogun_id '
                'LEFT JOIN degerlendirmeler d ON d.menu_id = m.id AND d.kullanici_id = r.kullanici_id '
                "WHERE r.kullanici_id = %s AND r.durum = 'kullanildi' "
                'ORDER BY m.tarih DESC, o.sira',
                (kullanici_id,))
            return imlec.fetchall()
    finally:
        baglanti.close()


def degerlendir(kullanici_id, menu_id, puan, yorum):
    
    baglanti = db.yazma()
    try:
        with baglanti.cursor() as imlec:
            try:
                imlec.execute(
                    'INSERT INTO degerlendirmeler (kullanici_id, menu_id, puan, yorum) '
                    'SELECT %s, %s, %s, %s FROM rezervasyonlar '
                    "WHERE kullanici_id = %s AND menu_id = %s AND durum = 'kullanildi' LIMIT 1",
                    (kullanici_id, menu_id, puan, yorum or None, kullanici_id, menu_id))
            except pymysql.err.IntegrityError as hata:
                if hata.args[0] == 1062:  # UNIQUE: уже оценено
                    raise IsKuraliHatasi('Bu menüyü zaten değerlendirdiniz.')
                raise
            if imlec.rowcount == 0:
                raise IsKuraliHatasi('Yalnızca kullandığınız menüyü değerlendirebilirsiniz.')
    finally:
        baglanti.close()