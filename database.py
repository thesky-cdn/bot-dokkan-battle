import requests
import config
import api.outgame as outgame
from pysqlsimplecipher import decryptor
import sqlite3
import os as fs

def download(ver, token, secret, version):
    if ver == 'gb':
        store = outgame.getDatabase(ver, token, secret, None)
        url = store['url']
        r = requests.get(url, allow_redirects=True)
        open('enc_gb.db', 'wb').write(r.content)
        p = config.gdb
        password = bytearray(p.encode('utf8'))
        print('decrypting... (this may take awhile.)')
        decryptor.decrypt_file('enc_gb.db', password, 'gb.db')
        fs.unlink('./enc_gb.db')
        f = open(ver + '-data.txt', 'w')
        f.write(str(version) + '\n')
        f.close()
    else:
        store = outgame.getDatabase(ver, token, secret, None)
        url = store['url']
        r = requests.get(url, allow_redirects=True)
        open('enc_jp.db', 'wb').write(r.content)
        p = config.jdb
        password = bytearray(p.encode('utf8'))
        print('decrypting... (this may take awhile.)')
        decryptor.decrypt_file('enc_jp.db', password, 'jp.db')
        fs.unlink('./enc_jp.db')
        f = open(ver + '-data.txt', 'w')
        f.write(str(version) + '\n')
        f.close()

def fetch(db, table, where):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    if where is not None:
        if 'jp.db' in db:
            con = sqlite3.connect('gb.db')
            curso = con.cursor()
            query = "SELECT * FROM " + table + " WHERE " + where
            try:
                curso.execute(query)
                results = curso.fetchone()
            except:
                results = None
            if results is None:
                query = "SELECT * FROM " + table + " WHERE " + where
                cursor.execute(query)
                results = cursor.fetchone()
        else:
            query = "SELECT * FROM " + table + " WHERE " + where
            cursor.execute(query)
            results = cursor.fetchone()
    else:
        if 'jp.db' in db:
            con = sqlite3.connect('gb.db')
            curso = con.cursor()
            query = "SELECT * FROM " + table
            try:
                curso.execute(query)
                results = curso.fetchall()
            except:
                results = None
            if results is None:
                query = "SELECT * FROM " + table
                cursor.execute(query)
                results = cursor.fetchall()
        else:
            query = "SELECT * FROM " + table
            cursor.execute(query)
            results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results