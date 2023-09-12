# System imports
from datetime import date
import json
import sys
sys.path.extend(['../'])

# Config imports
from config.config import Connections

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

    ### 
    # ISSUES INTERATIONS
    ###
class DatabaseInterface:
    # GETTERS
    def sms_count():
        cursor = Database().connect()
        cursor.execute("""SELECT COUNT(id) FROM SMSS;""")
        return cursor.fetchone()

    def sms_get():
        cursor = Database().connect()
        cursor.execute("""SELECT * FROM SMSS WHERE id=%s""", (id))
        return cursor.fetchone()
    
    def sms_get_all():
        cursor = Database().connect()
        cursor.execute("""select id,sender,receiver,msg,to_char(receive_date, 'DD/MM/YY HH24:MI:SS') FROM SMSS LIMIT 3000""")
        return cursor.fetchall()
    
    def sms_get_by_sender(sender):
        cursor = Database().connect()
        cursor.execute("""SELECT id,sender,receiver,msg,to_char(receive_date, 'DD/MM/YY HH24:MI:SS') FROM SMSS WHERE sender=%s""", (sender))
        return cursor.fetchall()
    
    def sms_get_by_receiver(receiver):
        cursor = Database().connect()
        cursor.execute("""SELECT id,sender,receiver,msg,to_char(receive_date, 'DD/MM/YY HH24:MI:SS') FROM SMSS WHERE receiver=%s""", (receiver))
        return cursor.fetchall()

    def sms_get_by_search(search):
        cursor = Database().connect()
        query = """SELECT id,sender,receiver,msg,to_char(receive_date, 'DD/MM/YY HH24:MI:SS') FROM SMSS WHERE LOWER(receiver) LIKE LOWER('%{}%') or LOWER(msg) LIKE LOWER('%{}%')""".format(search, search)
        cursor.execute(query)
        return cursor.fetchall()
    
    # SETTERS
    def sms_insert(sms):
        # Handle data
        columns = sms.getAttributes()
        try:
            values  = sms.getValuesForDatabase()
        except:
            raise
        query   = """ INSERT INTO SMSS(%s) VALUES(%s); """ % (columns, values)
        print(values)

        # Database call
        cursor = Database().connect()
        try:
            cursor.execute(query)
        except Exception as error:
            raise


    # CLEANERS
    def clean_database():
        cursor = Database().connect()
        query = """DELETE FROM SMSS;"""
        cursor.execute(query)
        print("Database cleaned!")    
