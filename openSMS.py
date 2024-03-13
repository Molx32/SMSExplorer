# System
import requests
import sys
from datetime import datetime
import time

from config.config import Config
from modules.interface import TargetInterface, ModuleInterface

# Database
from database.database import DatabaseInterface

# Temp
from database.models import SMS

# Flask
from flask import Flask
from flask import redirect, url_for, request
from flask import render_template
from flask import send_file
from flask import render_template_string
from flask import jsonify
import urllib.parse


# Redis
from redis import Redis
import rq
from rq.worker import Worker, WorkerStatus
from rq.command import send_kill_horse_command

# Send jobs to queue
redis_queue = Redis.from_url(Config.REDIS_URL)
task_queue  = rq.Queue(default_timeout=-1, connection=redis_queue)
task_queue.enqueue(DatabaseInterface.targets_initialize)
task_queue.enqueue(TargetInterface.create_instance_receivesmss)
task_queue.enqueue(ModuleInterface.create_instance_mock)

# Configure Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Populate database with configuration









# --------------------------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------- WEB PAGES ----------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------- #
# -                            HOME                               - #
# ----------------------------------------------------------------- #
@app.route("/")
@app.route("/home", methods = ['GET'])
def home():
    # Get statistics
    count_messages  = DatabaseInterface.sms_count_all()[0]
    count_urls      = DatabaseInterface.sms_count_all_urls()[0]
    count_data      = DatabaseInterface.sms_count_all_data()[0]
    count_unknown   = DatabaseInterface.sms_count_unknown()[0]

    # Activities
    activities_last_data = DatabaseInterface.sms_activities_last_data()

    # Load forms
    return render_template('home.html',
        count_messages=count_messages, count_urls=count_urls,
        count_data=count_data, count_unknown=count_unknown,
        activities_last_data=activities_last_data)


# ----------------------------------------------------------------- #
# -                      SEARCH ENDPOINT                          - #
# ----------------------------------------------------------------- #
@app.route("/search", methods = ['GET'])
def search():
    input_data          = request.args.get('input_data')
    input_interesting   = request.args.get('input_interesting')
    input_search        = request.args.get('search')


    # Check if input is safe
    if input_data not in Config.SEARCH_FILTERS_DATA:
        input_data = 'NONE'
    if input_interesting not in Config.SEARCH_FILTERS_INTERESTING:
        input_interesting = 'ALL'
    if input_search is None:
        input_search = ''

    # Upper case
    input_data = input_data.upper()
    input_interesting = input_interesting.upper()
    
    # Get SMSs
    data = DatabaseInterface.sms_get_by_search(input_search, input_data, input_interesting)
    total_count   = DatabaseInterface.sms_count()
    select_count  = len(data)

    return render_template('search.html', data=data, total_count=total_count, select_count=select_count)

# ----------------------------------------------------------------- #
# -                       SEARCH TARGETS                          - #
# ----------------------------------------------------------------- #
@app.route("/search_targets", methods = ['GET'])
def search_targets():
    input_search  = request.args.get('search')
    if input_search is None:
        input_search = ''

    # Get SMSs
    data    = DatabaseInterface.targets_get_all(input_search)
    count   = DatabaseInterface.targets_count()

    return render_template('targets.html', data=data, count=count)

# ---------------------------------------------------------------- #
# -                       INVESTIGATION                          - #
# ---------------------------------------------------------------- #
@app.route("/investigation", methods = ['GET'])
def investigation():
    # Get params
    input_search  = request.args.get('search')
    input_unique  = request.args.get('unique')

    # Filter params
    if input_search is None:
        input_search = ''
    if input_unique is None:
        input_unique = False
    if input_unique == 'YES':
        input_unique = True
    else:
        input_unique = False


    # Get SMSs
    data    = DatabaseInterface.sms_get_unqualified_targets(input_search, input_unique)
    count   = len(data)

    return render_template('investigation.html', data=data, count=count)

# ----------------------------------------------------------------- #
# -                    STATISTICS ENDPOINT                        - #
# ----------------------------------------------------------------- #
@app.route("/statistics_raw", methods = ['GET'])
def statistics_raw():
    # Chart - sms_get_count_by_hour
    sms_get_count_by_hour = DatabaseInterface.sms_get_count_by_hour()
    sms_get_count_by_hour_labels = [str(row[0]) for row in sms_get_count_by_hour]
    sms_get_count_by_hour_values = [str(row[1]) for row in sms_get_count_by_hour]

    sms_get_top_ten_domains = DatabaseInterface.sms_get_top_ten_domains()
    sms_get_top_ten_domains_labels = [str(row[0]) for row in sms_get_top_ten_domains]
    sms_get_top_ten_domains_values = [str(row[1]) for row in sms_get_top_ten_domains]

    sms_get_top_ten_countries = DatabaseInterface.sms_get_top_ten_countries()
    sms_get_top_ten_countries_labels = [str(row[0]) for row in sms_get_top_ten_countries]
    sms_get_top_ten_countries_values = [str(row[1]) for row in sms_get_top_ten_countries]


    return render_template('statistics_raw.html',
        sms_get_count_by_hour_values=sms_get_count_by_hour_values, sms_get_count_by_hour_labels=sms_get_count_by_hour_labels,
        sms_get_top_ten_domains_labels=sms_get_top_ten_domains_labels, sms_get_top_ten_domains_values=sms_get_top_ten_domains_values,
        sms_get_top_ten_countries_labels=sms_get_top_ten_countries_labels, sms_get_top_ten_countries_values=sms_get_top_ten_countries_values)

@app.route("/statistics_san", methods = ['GET'])
def statistics_san():
    sms_get_statistics_interesting = DatabaseInterface.sms_get_statistics_interesting()
    sms_get_statistics_interesting_labels = list(sms_get_statistics_interesting.keys())
    sms_get_statistics_interesting_values = list(sms_get_statistics_interesting.values())

    sms_get_statistics_interesting_tags_yes = DatabaseInterface.sms_get_statistics_interesting_tags_yes()
    sms_get_statistics_interesting_tags_yes_labels = list(sms_get_statistics_interesting_tags_yes.keys())
    sms_get_statistics_interesting_tags_yes_values = list(sms_get_statistics_interesting_tags_yes.values())

    sms_get_statistics_interesting_tags_no = DatabaseInterface.sms_get_statistics_interesting_tags_no()
    sms_get_statistics_interesting_tags_no_labels = list(sms_get_statistics_interesting_tags_no.keys())
    sms_get_statistics_interesting_tags_no_values = list(sms_get_statistics_interesting_tags_no.values())

    return render_template('statistics_san.html', 
        sms_get_statistics_interesting_labels=sms_get_statistics_interesting_labels, sms_get_statistics_interesting_values=sms_get_statistics_interesting_values,
        sms_get_statistics_interesting_tags_yes_labels=sms_get_statistics_interesting_tags_yes_labels, sms_get_statistics_interesting_tags_yes_values=sms_get_statistics_interesting_tags_yes_values,
        sms_get_statistics_interesting_tags_no_labels=sms_get_statistics_interesting_tags_no_labels, sms_get_statistics_interesting_tags_no_values=sms_get_statistics_interesting_tags_no_values)




# ----------------------------------------------------------------- #
# -                     SETTINGS ENDPOINT                         - #
# ----------------------------------------------------------------- #
@app.route("/settings", methods = ['GET'])
def settings():
    # Get settings


    # Load forms
    return render_template('settings.html')


@app.route("/settings/export_smss", methods = ['GET'])
def settings_export_smss():
    DatabaseInterface.export_smss()
    return send_file('/etc/data/exports.csv', as_attachment=True)

# @app.route("/settings/export_targets", methods = ['GET'])
# def settings_export_targets():
#     DatabaseInterface.export_smss()
#     return send_file('/etc/data/exports.csv', as_attachment=True)





# ----------------------------------------------------------------- #
# -                       ABOUT ENDPOINT                          - #
# ----------------------------------------------------------------- #
@app.route("/about", methods = ['GET'])
def about():
    return render_template('about.html')



# --------------------------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------- APIs ------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------- #
# -                       CLEAN DATABASE                          - #
# ----------------------------------------------------------------- #

@app.route("/api/get_data", methods = ['GET'])
def data():

    # Get searched SMSs
    if request.args.get('id'):
        sms_id = request.args.get('id')
        data = DatabaseInterface.sms_get_data_by_id(sms_id)[0]
        print(data)
        print(jsonify(data))
    # Get all SMSs
    else:
        data = {}
    return jsonify(data)


@app.route("/settings/database/clean", methods = ['GET'])
def clean():
    workers = Worker.all(redis)
    for worker in workers:
        send_kill_horse_command(redis, worker.name)
    time.sleep(2)
    DatabaseInterface.clean_database()
    # Relaunch workers
    task_queue.enqueue(DatabaseInterface.targets_initialize)
    task_queue.enqueue(TargetInterface.create_instance_receivesmss)
    task_queue.enqueue(ModuleInterface.create_instance_mock)

@app.route("/settings/database/targets_update", methods = ['GET'])
def targets_update():
    pass

@app.template_filter('decode')
def decode_msg(encoded):
    decoded = urllib.parse.unquote_plus(encoded)
    decoded = decoded.replace("%26", "&")
    return decoded


