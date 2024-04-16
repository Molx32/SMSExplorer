# System imports
from datetime import date
import json
import csv
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
    def is_database_healthy():
        try:
            Database().connect()
        except Exception as e:
            raise e


############################### SMSS & DATA ######################################
# The following section is dedicated to SQL request that read or write SMS table #
##################################################################################
    # GETTERS
    def sms_get_by_search(search, input_data, input_interesting):
        cursor = Database().connect()
        excluded_domains = "'" + "','".join(Config.EXCLUDED_DOMAINS) + "'"

        # SELECT 
        select  = ""
        select  = select + "SELECT "
        select  = select + "smss.id, to_char(smss.receive_date, 'DD/MM/YY HH24:MI:SS'), sender, receiver, msg, country, url, smss.domain, data_handled, is_interesting, is_automated, is_interesting_desc """
        select  = select + "FROM smss "

        # JOIN
        join    = "LEFT OUTER JOIN targets ON smss.domain = targets.domain "

        # WHERE
        where   = "WHERE "
        where   = where + """smss.domain NOT IN ({}) """.format(excluded_domains)


        # Handle Search
        if search != '' and search is not None:
            where   = where + """AND (LOWER(receiver) LIKE LOWER('%{}%') or LOWER(msg) LIKE LOWER('%{}%')) """.format(search, search)

        # Handle data filter
        if input_data == 'ALL' or input_data == '' or input_data is None:
            where = where + ""
        if input_data == 'YES':
            where = where + " AND data_handled = True "
        if input_data == 'NO':
            where = where + " AND data_handled = False "

        # Handle interesting filter
        if input_interesting == 'ALL' or input_interesting == '' or input_interesting is None:
            where = where + ""
        elif input_interesting == 'NONE':
            where = where + " AND is_interesting IS NULL "
        elif input_interesting == 'YES':
            where = where + " AND is_interesting = True "
        elif input_interesting == 'NO':
            where = where + " AND is_interesting = False "

        order_by            = """ ORDER BY receive_date DESC """.format(search, search, excluded_domains)
        limit               = """ LIMIT 1000 """
        query = select + join + where + order_by + limit
        print(query)
        cursor.execute(query)
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

    def sms_insert_data(sms_id, json_data):
        try:
            cursor = Database().connect()
            query   = """ INSERT INTO DATA(SMS_DATA,SMS_ID) VALUES('{}', {}); """.format(json_data, sms_id)
            cursor.execute(query)

            # Update row
            query   = """ UPDATE SMSS SET data_handled = True WHERE id = {}""".format(sms_id)
            cursor.execute(query)
        except Exception as e:
            raise e


############################# STATISTICS ###################################
# The following section is dedicated to SQL request that handle statistics #
############################################################################
    def sms_count():
        cursor = Database().connect()
        cursor.execute("""SELECT COUNT(id) FROM SMSS;""")
        return cursor.fetchone()

    def sms_get_count_by_hour(sanitized=False):
        # Default query
        select  = "SELECT to_char(DATE_TRUNC('hour', receive_date), 'DD/MM/YY HH24:MI:SS') as hour, COUNT(id) FROM SMSS"
        where   = ""
        end     = " GROUP BY 1 ORDER BY 1 ASC LIMIT 744;"

        # Sanitized query
        if sanitized:
            excluded_domains = "'" + "','".join(Config.EXCLUDED_DOMAINS) + "'"
            where = where + """ WHERE smss.domain NOT IN ({})""".format(excluded_domains)

        # Execute
        query   = select + where + end
        cursor  = Database().connect()
        cursor.execute(query)
        return cursor.fetchall()

    def sms_get_top_ten_domains(sanitized=False):
        # Default query
        select  = "SELECT domain, COUNT(id) FROM SMSS"
        where   = " WHERE domain != ''"
        end     = " GROUP BY 1 ORDER BY 2 DESC;"

        # Sanitized query
        if sanitized:
            excluded_domains = "'" + "','".join(Config.EXCLUDED_DOMAINS) + "'"
            where = where + """ AND smss.domain NOT IN ({})""".format(excluded_domains)

        # Execute
        query   = select + where + end
        cursor  = Database().connect()
        cursor.execute(query)
        return cursor.fetchall()
    
    def sms_get_top_ten_countries(sanitized=False):
        # Default query
        select  = "SELECT country, COUNT(id) FROM SMSS"
        where   = ""
        end     = " GROUP BY 1 ORDER BY 2 DESC;"

        # Sanitized query
        if sanitized:
            excluded_domains = "'" + "','".join(Config.EXCLUDED_DOMAINS) + "'"
            where   = where + """ WHERE smss.domain NOT IN ({})""".format(excluded_domains)

        # Execute
        query   = select + where + end
        cursor  = Database().connect()
        cursor.execute(query)
        return cursor.fetchall()

    def data_get_count_by_hour(sanitized=False):
        # Default query
        select  = "SELECT to_char(DATE_TRUNC('hour', receive_date), 'DD/MM/YY HH24:MI:SS') as hour, COUNT(id) FROM smss"
        where   = " WHERE data_handled = True"
        end     = " GROUP BY 1 ORDER BY 1 ASC LIMIT 744;"

        # Execute
        query   = select + where + end
        cursor  = Database().connect()
        cursor.execute(query)
        return cursor.fetchall()

    def data_get_url_count_by_hour(sanitized=False):
        # Default query
        select  = "SELECT to_char(DATE_TRUNC('hour', receive_date), 'DD/MM/YY HH24:MI:SS') as hour, COUNT(id) FROM smss"
        where   = " WHERE url <> '' and url IS NOT NULL"
        end     = " GROUP BY 1 ORDER BY 1 ASC LIMIT 744;"

        # Execute
        query   = select + where + end
        cursor  = Database().connect()
        cursor.execute(query)
        return cursor.fetchall()

    def data_get_count_by_category(sanitized=False):
        # Default query
        query  = "select count(smss.id), targets.domain, is_interesting,is_interesting_desc from targets join smss on smss.domain = targets.domain GROUP BY targets.domain, is_interesting, is_interesting_desc"
        # Execute
        cursor  = Database().connect()
        cursor.execute(query)
        return cursor.fetchall()

    def data_get_top_ten_domains(sanitized=False):
        # Default query
        select  = "SELECT domain, COUNT(id) FROM SMSS"
        where   = " WHERE domain != '' AND data_handled = True"
        end     = " GROUP BY 1 ORDER BY 2 DESC;"

        # Execute
        query   = select + where + end
        cursor  = Database().connect()
        cursor.execute(query)
        return cursor.fetchall()
    
    def data_get_top_ten_countries(sanitized=False):
        # Default query
        select  = "SELECT country, COUNT(id) FROM SMSS"
        where   = " WHERE domain != '' AND data_handled = True"
        end     = " GROUP BY 1 ORDER BY 2 DESC;"

        # Execute
        query   = select + where + end
        cursor  = Database().connect()
        cursor.execute(query)
        return cursor.fetchall()

################################### HOME ###################################
# The following section is dedicated to SQL request that handle the home   #
# page, event if it also includes statistics.                              #
############################################################################
    def sms_count_all():
        cursor = Database().connect()
        cursor.execute("SELECT COUNT(id) FROM SMSS;")
        return cursor.fetchone()
    
    def sms_count_all_data():
        cursor = Database().connect()
        cursor.execute("SELECT COUNT(id) FROM SMSS WHERE data_handled = 't';")
        return cursor.fetchone()

    def sms_count_all_urls():
        cursor = Database().connect()
        cursor.execute("SELECT COUNT(id) FROM SMSS WHERE URL <> '';")
        return cursor.fetchone()

    def sms_count_unknown():
        cursor = Database().connect()
        cursor.execute("SELECT COUNT(id) FROM SMSS WHERE URL = '';")
        return cursor.fetchone()

    def sms_activities_last_data():
        cursor = Database().connect()
        cursor.execute("SELECT id, to_char(smss.receive_date, 'DD/MM/YY HH24:MI:SS'), sender, receiver, msg, country FROM SMSS WHERE data_handled = 't' LIMIT 5;")
        return cursor.fetchall()

    def sms_get_statistics_interesting():
        # All -> URLs -> Interesting
        def _count_all_interesting(is_interesting):
            query = ""
            if is_interesting == Config.METADATA_INTERESTING_YES:
                query = "SELECT COUNT(smss.id) FROM SMSS LEFT OUTER JOIN targets ON smss.domain = targets.domain WHERE is_interesting = True"
            elif is_interesting == Config.METADATA_INTERESTING_NO:
                query = "SELECT COUNT(smss.id) FROM SMSS LEFT OUTER JOIN targets ON smss.domain = targets.domain WHERE is_interesting = False"
            elif is_interesting == Config.METADATA_INTERESTING_UNKNOWN:
                query = "SELECT COUNT(smss.id) FROM SMSS LEFT OUTER JOIN targets ON smss.domain = targets.domain WHERE is_interesting is null"

            cursor = Database().connect()
            cursor.execute(query)
            return cursor.fetchone()

        r = {}
        for is_interesting in Config.LIST_METADATA_INTERESTING:
            r[is_interesting] = _count_all_interesting(is_interesting)[0]
        return r

    def sms_get_statistics_interesting_tags_yes():
        # All -> URLs -> Interesting
        def _count_all_interesting_tag(tag):
            cursor = Database().connect()
            cursor.execute("SELECT COUNT(smss.id) FROM SMSS LEFT OUTER JOIN targets ON smss.domain = targets.domain WHERE is_interesting_desc LIKE '%{}%'".format(tag))
            return cursor.fetchone()

        r = {}
        for tag in Config.LIST_METADATA_INTERESTING_YES:
            r[tag] = _count_all_interesting_tag(tag)[0]
        return r

    def sms_get_statistics_interesting_tags_no():
        # All -> URLs -> Interesting
        def _count_all_interesting_tag(tag):
            cursor = Database().connect()
            cursor.execute("SELECT COUNT(smss.id) FROM SMSS LEFT OUTER JOIN targets ON smss.domain = targets.domain WHERE is_interesting_desc LIKE '%{}%'".format(tag))
            return cursor.fetchone()

        r = {}
        for tag in Config.LIST_METADATA_INTERESTING_NO:
            r[tag] = _count_all_interesting_tag(tag)[0]
        return r

############################### INVESTIGATION ##############################
# The following section is dedicated to the investigation pane, where      #
# targets can be modified.                                                 #
############################################################################
    def sms_get_targets(search, unqualified):
        select  = "SELECT min(targets.id), min(smss.url), min(smss.msg), min(smss.domain), bool_or(targets.is_interesting), min(targets.is_interesting_desc) FROM smss LEFT OUTER JOIN targets ON smss.domain = targets.domain "
        where = ""
        group_by = "GROUP BY smss.domain LIMIT 200;"

        if not search:
            search = ''

        # Handled 'where'
        if unqualified == 'YES':
            where = "WHERE LOWER(smss.domain) LIKE LOWER('%{}%') AND (is_interesting IS NULL or is_interesting_desc = '') AND url <> '' """.format(search)
        else:
            where = "WHERE LOWER(smss.domain) LIKE LOWER('%{}%') AND url <> '' """.format(search)

        query   = select + where + group_by

        # Handle Search
        cursor = Database().connect()
        cursor.execute(query)
        return cursor.fetchall()

############################### DATA WORKER ################################
# The following section is dedicated to SQL queries used by the data       #
# worker, which needs to review all interesting URLs found in modules.     #
############################################################################
    # DATA HANDLERS
    def get_sms_by_url(url):
        cursor = Database().connect()
        cursor.execute("""SELECT id,url,msg FROM SMSS WHERE URL LIKE '{}%' AND DATA_HANDLED=False;""".format(url))
        return cursor.fetchall()



############################# AUTOMATION ###################################
# The following section is dedicated to SQL queries used by the automation #
# view, but not by the investigation one!                                  #
############################################################################
    def automation_get_targets(search, is_legal, is_automated):
        # SELECT
        select = "SELECT id, domain, is_legal, is_automated, is_interesting, is_interesting_desc FROM TARGETS"
        # WHERE
        where = " WHERE is_interesting = True"
        if search != '':
            where = where + " AND LOWER(domain) LIKE LOWER('%{}%')".format(search)
        if is_legal is not None:
            where = where + " AND is_legal = {}".format(is_legal)
        if is_automated is not None:
            where = where + " AND is_automated = {}".format(is_automated)
        # LIMIT
        limit = " LIMIT 200"

        query = select + where + limit
        cursor = Database().connect()
        cursor.execute(query)
        return cursor.fetchall()

    def targets_count():
        cursor = Database().connect()
        cursor.execute('SELECT COUNT(id) FROM TARGETS;')
        return cursor.fetchone()

    def targets_has_been_init():
        # Connect to database
        cursor = Database().connect()

        # If targets has already been init, return True
        query   = "SELECT is_targets_imported FROM CONFIG"
        cursor.execute(query)
        res = cursor.fetchone()[0]
        return res
        
    def targets_update_automation(domain, is_legal, is_automated):


        # Check if target exists
        query = """SELECT id FROM targets WHERE domain = '{}';""".format(domain)
        cursor = Database().connect()
        cursor.execute(query)
        results = cursor.fetchone()
        if not results:
            query   = """INSERT INTO TARGETS(DOMAIN, IS_LEGAL, IS_AUTOMATED) VALUES('{}', '{}', '{}'); """.format(domain, is_legal, is_automated)
            cursor.execute(query)
        else:
            query = """UPDATE targets SET is_legal = {}, is_automated = {}  WHERE domain = '{}'""".format(is_legal, is_automated, domain)
            cursor.execute(query)

    def targets_update_categorize(domain, is_interesting, tags):
        # Check if target exists
        query = """SELECT id FROM targets WHERE domain = '{}';""".format(domain)
        cursor = Database().connect()
        cursor.execute(query)
        results = cursor.fetchone()
        if not results:
            query   = """INSERT INTO TARGETS(DOMAIN, IS_LEGAL, IS_AUTOMATED, IS_INTERESTING, IS_INTERESTING_DESC) VALUES('{}', '{}', '{}', '{}', '{}'); """.format(domain, False, False, is_interesting, tags)
            cursor.execute(query)
        else:
            query = """UPDATE targets SET is_interesting = {}, is_interesting_desc = '{}'  WHERE domain = '{}'""".format(is_interesting, tags, domain)
            cursor.execute(query)

############################### SETTINGS ###################################
# Well, all options accessible using the settings page.                    #
############################################################################
    def export_smss():
        cursor = Database().connect()
        with open(Config.EXPORT_SMSS, 'a') as f:
            cursor.copy_expert("COPY smss TO STDOUT WITH CSV DELIMITER ';' HEADER", f)
        return

    def export_targets():
        cursor = Database().connect()
        with open(Config.EXPORT_TARGETS, 'a') as f:
            cursor.copy_expert("COPY targets TO STDOUT WITH CSV DELIMITER ';' HEADER", f)
        return

    def export_data():
        cursor = Database().connect()
        with open(Config.EXPORT_DATA, 'a') as f:
            cursor.copy_expert("COPY data TO STDOUT WITH CSV DELIMITER ';' HEADER", f)
        return

    def export_config():
        cursor = Database().connect()
        with open(Config.EXPORT_CONFIG, 'a') as f:
            cursor.copy_expert("COPY config TO STDOUT WITH CSV DELIMITER ';' HEADER", f)
        return
    
    def targets_update(file_path):
        cursor = Database().connect()
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar=' ')
            next(reader, None)
            for row in reader:
                domain              = row[1]
                is_legal            = row[2]
                is_automated        = row[3]
                is_interesting      = row[4]
                is_interesting_desc = row[5]
                query   = """INSERT INTO TARGETS(DOMAIN, IS_LEGAL, IS_AUTOMATED, IS_INTERESTING, IS_INTERESTING_DESC) VALUES('{}', '{}','{}', '{}', '{}'); """.format(domain, is_legal, is_automated, is_interesting, is_interesting_desc)
                try:
                    cursor.execute(query)
                except:
                    continue
    
    def switch_mode(mode):
        query = """UPDATE config SET mode = '{}'""".format(mode)
        cursor = Database().connect()
        cursor.execute(query)

    def get_mode():
        query = "SELECT mode FROM config"
        cursor = Database().connect()
        cursor.execute(query)
        return cursor.fetchone()[0]
    
    def clean_database():
        cursor = Database().connect()
        query = """DELETE FROM SMSS;"""
        cursor.execute(query)
        print("Database cleaned!")

############################### SETTINGS ###################################
# Well, all options accessible using the settings page.                    #
############################################################################
    def sms_get_supported_targets():
        query  = "SELECT domain, is_legal FROM targets WHERE is_automated = True;" 

        # Handle Search
        cursor = Database().connect()
        cursor.execute(query)
        return cursor.fetchall()