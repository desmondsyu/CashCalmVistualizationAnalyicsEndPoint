import mysql.connector
import json
from fastapi import HTTPException, status







class Connector:
    def __init__(self):
        with open('config.json') as config_file:
            config = json.load(config_file)
            self.host = config['database']['host']
            self.database = config['database']['database']
            self.user = config['database']['user']
            self.password = config['database']['password']
            self.con = None

    def _connect(self):
        try:
            self.con = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as err:
            print(str(err))

    def disconnect(self):
        if self.con:
            self.con.close()

    def execute(self, sql):
        self._connect()
        cur = self.con.cursor()
        try:
            cur.execute(sql)
            result = cur.fetchall()
            return result if len(result) > 0 else None
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            cur.close()
            self.disconnect()
