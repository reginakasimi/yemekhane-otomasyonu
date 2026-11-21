from web import db


def tum_alerjenler():
    
    baglanti = db.okuma()
    try:
        with baglanti.cursor() as imlec:
            imlec.execute('SELECT id, ad FROM alerjenler ORDER BY ad')
            return imlec.fetchall()
    finally:
        baglanti.close()


def secili_alerjen_idleri(kullanici_id):
    
    baglanti = db.yazma()
    try:
        with baglanti.cursor() as imlec:
            imlec.execute('SELECT alerjen_id FROM kullanici_alerjenleri WHERE kullanici_id = %s',
                          (kullanici_id,))
            return {s['alerjen_id'] for s in imlec.fetchall()}
    finally:
        baglanti.close()


def alerjenleri_kaydet(kullanici_id, alerjen_idleri):
    baglanti = db.yazma()
    try:
        baglanti.begin()
        with baglanti.cursor() as imlec:
            imlec.execute('DELETE FROM kullanici_alerjenleri WHERE kullanici_id = %s', (kullanici_id,))
            for aid in alerjen_idleri:
                imlec.execute(
                    'INSERT INTO kullanici_alerjenleri (kullanici_id, alerjen_id) VALUES (%s, %s)',
                    (kullanici_id, aid))
        baglanti.commit()
    except Exception:
        baglanti.rollback()
        raise
    finally:
        baglanti.close()