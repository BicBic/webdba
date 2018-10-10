#  ____  _      ____  _
# | __ )(_) ___| __ )(_) ___
# |  _ \| |/ __|  _ \| |/ __|
# | |_) | | (__| |_) | | (__
# |____/|_|\___|____/|_|\___|
import pyodbc
import os
import sys
import base64
from django.db import models
from django.core.files import File
from datetime import datetime 
from decouple import config

# Create your models here.
class configfile():
    def __init__(self):
        try:
            self.SECRET_KEY = config('SECRET_KEY')
            #BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            #print (BASE_DIR)

        except:
            print('ERROR: Caught exception: ')
            # raise e
            sys.exit(1)

    def item(self, item, decrip='1'):
        buffer = config(item)
        if '1' in decrip:
            buffer = self.decode(self.SECRET_KEY, buffer)
        
        return buffer

    def encode(self, key, clear):
        enc = []
        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc).encode()).decode()

    def decode(self, key, enc):
        dec = []
        enc = base64.urlsafe_b64decode(enc).decode()
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)


class log():
    def __init__(self, buffer):
    # def fWrite(self, buffer):
        pwd = os.path.dirname(__file__)
        file_path = os.path.join(pwd, 'log.txt')
        ts = datetime.now()
        with open(file_path, 'a') as f:
            myfile = File(f)
            myfile.write(str(ts.strftime("%y/%m/%d %H:%M:%S")) + ' ' + buffer + '\n')

        myfile.closed
        f.close
        return

class SQLpy():
    def __init__(self, servidor, banco='DBA', usuario='sa', senha=''):
        try:
            self.server = servidor
            self.db = banco
            self.user = usuario
            self.password = senha

        except:
            print('Erro...')
            # sys.exit(1)

    def Servidor(self, servidor):
        self.server = servidor

    def Banco(self, banco):
        self.db = banco

    def execute(self, sql=''):
        try:
            # self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};' + \
            #                       'server='+self.server+';database='+self.db+';Trusted_Connection=yes;autocommit=True' + \
            #                       'appname=CheckBackupPython;as_dict=True')
            self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.db+';UID='+self.user+';PWD='+self.password+';autocommit=True' + \
                        'appname=CheckBackupPython;as_dict=True')
        except:
            self.conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+self.server+';DATABASE='+self.db+';UID='+self.user+';PWD='+self.password+';autocommit=True' + \
                                  'appname=CheckBackupPython;as_dict=True')

        cursor = self.conn.cursor()

        rows = cursor.execute(sql)

##        recs = cursor.fetchall()
##        rows = [dict(rec) for rec in recs[0]]
##        rows = []
##        for row in recs:
##            rows.append(list(row))
            
        return rows

    def close(self):
        self.conn.close()
        
class Post():
    ccProducao = '1'
    ccDTH = '1'

    def __str__(self):
        return self.ccProducao
