import os

import pymysql
from pymysql.cursors import DictCursor


def _baglan(host):
    return pymysql.connect(
        host=host,
        port=int(os.environ.get('DB_PORT', '3306')),
        user=os.environ['DB_KULLANICI'],
        password=os.environ['DB_SIFRE'],
        database=os.environ['DB_ADI'],
        charset='utf8mb4',
        autocommit=True,
        cursorclass=DictCursor,
        connect_timeout=5,
    )


def yazma():
    """Источник (mysql-primary): все записи и вызовы процедур."""
    return _baglan(os.environ['DB_YAZMA_HOST'])


def okuma():
    """Реплика (mysql-replica): списки и отчёты."""
    return _baglan(os.environ['DB_OKUMA_HOST'])