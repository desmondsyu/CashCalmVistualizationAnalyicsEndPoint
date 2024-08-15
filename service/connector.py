import json
import mysql.connector
from fastapi import HTTPException, status


class Connector:
    def __init__(self, config_path='.connection.json'):
        self._load_config(config_path)
        self.con = None

    def _load_config(self, config_path):
        try:
            with open(config_path) as config_file:
                config = json.load(config_file)
                self.host = config['database']['hostname']
                self.database = config['database']['database']
                self.user = config['database']['user']
                self.password = config['database']['password']
        except FileNotFoundError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Configuration file not found")
        except json.JSONDecodeError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Invalid configuration file format")

    def _connect(self):
        try:
            if self.con is None or not self.con.is_connected():
                self.con = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    auth_plugin='mysql_native_password'
                )
        except mysql.connector.Error as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database connection error: {str(err)}")

    def disconnect(self):
        if self.con is not None and self.con.is_connected():
            self.con.close()
            self.con = None

    def execute(self, sql, params=None):
        self._connect()
        cur = self.con.cursor()
        try:
            cur.execute(sql, params or ())

            if sql.strip().upper().startswith("SELECT"):
                result = cur.fetchall()
                return result
            else:
                self.con.commit()
                return cur.rowcount

        except mysql.connector.Error as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(err)}")
        finally:
            cur.close()
            self.disconnect()
