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
from flask import render_template_string
from flask import jsonify
from forms.forms import SearchForm
import urllib.parse


# Redis
from redis import Redis
import rq
from rq.worker import Worker, WorkerStatus
from rq.command import send_kill_horse_command

# Send jobs to queue
redis_queue = Redis.from_url(Config.REDIS_URL)
task_queue  = rq.Queue(default_timeout=-1, connection=redis_queue)
task_queue.enqueue(TargetInterface.create_instance_receivesmss)
task_queue.enqueue(ModuleInterface.create_instance_mock)

# Configure Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY









# --------------------------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------- WEB PAGES ----------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------- #
# -                      SEARCH ENDPOINT                          - #
# ----------------------------------------------------------------- #
def _generic_search(is_raw=False):
    # Get searched SMSs
    if request.args.get('search'):
        search = request.args.get('search')
        data = DatabaseInterface.sms_get_by_search(search, is_raw)
        count   = DatabaseInterface.sms_count()
    # Get all SMSs
    else:
        data = DatabaseInterface.sms_get_all(is_raw)
        count = DatabaseInterface.sms_count()

    # Load forms
    form    = SearchForm()
    return render_template('search.html', form=form, data=data, count=count)

@app.route("/")
    return redirect('/search_raw')

@app.route("/search_raw", methods = ['GET'])
def search_raw():
    return _generic_search(is_raw=True)

@app.route("/search_san", methods = ['GET'])
def search_san():
    return _generic_search(is_raw=False)



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

@app.route("/clean", methods = ['GET'])
def clean():
    workers = Worker.all(redis)
    for worker in workers:
        send_kill_horse_command(redis, worker.name)
    time.sleep(2)
    DatabaseInterface.clean_database()
    # Relaunch workers
    task_queue.enqueue(TargetInterface.create_instance_receivesmss)
    return redirect('/search')


@app.template_filter('decode')
def decode_msg(encoded):
    decoded = urllib.parse.unquote_plus(encoded)
    decoded = decoded.replace("%26", "&")
    return decoded


