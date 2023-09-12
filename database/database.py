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
    def sms_get():
        cursor = Database().connect()
        cursor.execute("""SELECT * FROM SMSS WHERE id=%s""", (id))
        return cursor.fetchone()
    
    def sms_get_all():
        cursor = Database().connect()
        cursor.execute("""select id,sender,receiver,msg,to_char(receive_date, 'DD/MM/YY HH24:MI:SS') FROM SMSS""")
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
        values  = sms.getValuesForDatabase()
        query   = """ INSERT INTO SMSS(%s) VALUES(%s); """ % (columns, values)

        # Database call
        cursor = Database().connect()
        cursor.execute(query)
        print("Call done")

    # CLEANERS
    def clean_database():
        cursor = Database().connect()
        query = """DROP DATABASE IF EXISTS SMSS"""
        cursor.execute(query)
        query = """CREATE TABLE SMSS(
                ID SERIAL PRIMARY KEY,
                SENDER VARCHAR(100),
                RECEIVER VARCHAR(100),
                MSG VARCHAR(5000),
                RECEIVE_DATE DATE
                );"""
        print("Database cleaned!")    
