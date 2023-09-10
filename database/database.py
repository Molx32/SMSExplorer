import sys
sys.path.extend(['../'])

from config.config import Connections
import psycopg2

# System imports
from datetime import date
import json

from database.models import SMS

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

    def drop(self):
        # Drop all tables
        self.ISSUES.drop()
        self.IMAGES.drop()

    def clean_issues(self):
        self.FILES.clean()
    
    def clean_images(self):
        self.IMAGES.clean()
 
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
        cursor.execute("""SELECT * FROM SMSS ORDER BY issue_id ASC""")
        return cursor.fetchall()
    
    def sms_get_by_sender(sender):
        cursor = Database().connect()
        cursor.execute("""SELECT * FROM SMSS WHERE sender=%s""", (sender))
        return cursor.fetchall()
    
    def sms_get_by_receiver(receiver):
        cursor = Database().connect()
        cursor.execute("""SELECT * FROM SMSS WHERE receiver=%s""", (receiver))
        return cursor.fetchall()
    
    # SETTERS
    def sms_insert(issue):
        # Handle data
        columns = issue.getAttributes()
        values  = issue.getValues()
        query   = """ INSERT INTO Issue(%s) VALUES(%s); """ % (columns, values)

        # Database call
        cursor = Database().connect()
        cursor.execute(query)
        print("Call done")