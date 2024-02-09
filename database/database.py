# System imports
from datetime import date
import json
import sys
sys.path.extend(['../'])

# Config imports
from config.config import Connections
from config.config import Logger
from config.config import Config

# Database imports
from database.models import SMS
import psycopg2
import urllib.parse

#####
# This class is used as an interface to communicate with the database.
# Any interaction with the database should be done using this class.
# Additionnaly, this class should not manipulate data, but only add/remove/update it.
#####
class Database:
    def __init__(self):
        # Connect to DB
        self.conn = None
        self.cursor = None

    ### 
    # DATABASE MANAGEMENT METHODS
    ### 
    def connect(self):
        # Connect to DB
        self.conn = psycopg2.connect(database=Connections.DATABASE, user=Connections.USER, password=Connections.PASSWORD, host=Connections.HOST, port=Connections.PORT)
        self.conn.autocommit = True
        # Init cursor
        self.cursor = self.conn.cursor()
        return self.cursor

    def disconnect(self):
        self.conn.close()
        self.cursor = None
        self.conn = None

class DatabaseInterface:
    # INIT
    def db_init():
        cursor = Database().connect()
        cursor.execute("""ALTER DATABASE SMSS SET datestyle TO 'GERMAN,MDY';""")
        print(cursor.fetchone())

    # GETTERS
    def sms_get():
        cursor = Database().connect()
        cursor.execute("""SELECT * FROM SMSS WHERE id=%s""", (id))
        return cursor.fetchone()
    
    def sms_get_all():
        cursor = Database().connect()
        excluded_domains = "'" + "','".join(Config.EXCLUDED_DOMAINS) + "'"
        cursor.execute("""SELECT id,sender,receiver,msg,to_char(receive_date, 'DD/MM/YY HH24:MI:SS'),country, url, domain, source, data_handled FROM SMSS WHERE domain NOT IN ({}) ORDER BY receive_date DESC LIMIT 1000;""".format(excluded_domains))
        return cursor.fetchall()
    
    def sms_get_by_search(search):
        cursor = Database().connect()
        excluded_domains = "'" + "','".join(Config.EXCLUDED_DOMAINS) + "'"
        query = """SELECT id,sender,receiver,msg,to_char(receive_date, 'DD/MM/YY HH24:MI:SS'), country, url, domain, source, data_handled FROM SMSS WHERE (LOWER(receiver) LIKE LOWER('%{}%') or LOWER(msg) LIKE LOWER('%{}%')) AND domain NOT IN ({}) ORDER BY receive_date DESC""".format(search, search, excluded_domains)
        cursor.execute(query)
        return cursor.fetchall()
    
    def sms_get_by_sender(sender):
        cursor = Database().connect()
        cursor.execute("""SELECT id,sender,receiver,msg,to_char(receive_date, 'DD/MM/YY HH24:MI:SS'), source, domain, url FROM SMSS WHERE sender=%s""", (sender))
        return cursor.fetchall()
    
    def sms_get_by_receiver(receiver):
        cursor = Database().connect()
        cursor.execute("""SELECT id,sender,receiver,msg,to_char(receive_date, 'DD/MM/YY HH24:MI:SS'), source, domain, url FROM SMSS WHERE receiver=%s""", (receiver))
        return cursor.fetchall()

    def sms_get_data_by_id(sms_id):
        cursor = Database().connect()
        cursor.execute("""SELECT sms_data FROM Data WHERE sms_id = {};""".format(sms_id))
        return cursor.fetchone()
        
    # SETTERS
    def sms_insert(sms):
        # Handle data
        columns = sms.getAttributes()
        try:
            values  = sms.getValuesForDatabase()
        except Exception as e:
            raise e
        query   = """ INSERT INTO SMSS(%s) VALUES(%s); """ % (columns, values)

        # Database call
        cursor = Database().connect()
        try:
            cursor.execute(query)
        except Exception as e:
            raise e

    def sms_data_insert(sms_id, json_data):
        try:
            cursor = Database().connect()
            query   = """ INSERT INTO DATA(SMS_DATA,SMS_ID) VALUES('{}', {}); """.format(json_data, sms_id)
            cursor.execute(query)

            # Update row
            query   = """ UPDATE SMSS SET data_handled = True WHERE id = {}""".format(sms_id)
            cursor.execute(query)
        except Exception as e:
            raise e

    # RAW STATISTICS
    def sms_count():
        cursor = Database().connect()
        cursor.execute("""SELECT COUNT(id) FROM SMSS;""")
        return cursor.fetchone()

    def sms_get_count_by_hour():
        cursor = Database().connect()
        cursor.execute("""SELECT to_char(DATE_TRUNC('hour', receive_date), 'DD/MM/YY HH24:MI:SS') as hour, COUNT(id) FROM SMSS GROUP BY 1 ORDER BY 1 ASC;""")
        return cursor.fetchall()

    def sms_get_top_ten_domains():
        cursor = Database().connect()
        cursor.execute("""SELECT domain, COUNT(id) FROM SMSS WHERE domain != '-'GROUP BY 1 ORDER BY 2 DESC;""")
        return cursor.fetchall()
    
    def sms_get_top_ten_countries():
        cursor = Database().connect()
        cursor.execute("""SELECT country, COUNT(id) FROM SMSS GROUP BY 1 ORDER BY 2 DESC;""")
        return cursor.fetchall()
    
    # SANITIZED STATISTICS
    # TODO

    # DATA HANDLERS
    def get_sms_by_url(url):
        cursor = Database().connect()
        cursor.execute("""SELECT id,url FROM SMSS WHERE URL LIKE '{}%' AND DATA_HANDLED=False;""".format(url))
        return cursor.fetchall()
    




    # CLEANERS
    def clean_database():
        cursor = Database().connect()
        query = """DELETE FROM SMSS;"""
        cursor.execute(query)
        print("Database cleaned!")    
