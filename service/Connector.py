from errno import errorcode

import mysql.connector
import json








class Connector:
    host = None
    user = None
    password = None
    database = None
    con = None

    def __init__(self):
        with open('../.connection.json') as config_file:
            config = json.load(config_file)
            self.host = config[0]['host']
            self.database = config[0]['data']
            self.user = config[0]['user']
            self.password = config[0]['password']

    def _connect(self):
        try:
            con = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            con.close()

    def disconnect(self):
        self.con.close()

    def execute(self, sql):
        self.connect()
        cur = self.con.cursor()
        try:
            cur.execute(sql)
            return cur.fetchall()
        except mysql.connector.Error as err:
            return str(err)

        finally:
            cur.close()
            self.disconnect()
