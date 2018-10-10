import pyodbc

class SQLpy():
    def __init__(self, servidor, banco='DBA'):
        try:
            self.server = servidor
            self.db = banco

        except:
            print('Erro...')
            # sys.exit(1)

    def Servidor(self, servidor):
        self.server = servidor

    def Banco(self, banco):
        self.db = banco

    def execute(self, sql=''):
        try:
            self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};' + \
                                  'server='+self.server+';database='+self.db+';Trusted_Connection=yes;autocommit=True' + \
                                  'appname=CheckBackupPython;as_dict=True')
        except:
            self.conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+self.server+';DATABASE='+self.db+';UID=sa;PWD=K*(&yucat_Ver0;autocommit=True' + \
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
        
