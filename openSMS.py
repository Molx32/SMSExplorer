# System
import requests
import sys
from datetime import datetime
import time
import json
import shutil

from config.config import Config
from modules.interface import TargetInterface, DataInterface, SecurityInterface

# Database
from database.database import DatabaseInterface

# Temp
from database.models import SMS

# Flask
from flask import Flask, abort
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
from rq.command import send_stop_job_command
from rq.registry import StartedJobRegistry


# --------------------------------------------------------------------- #
# -                            START UP                               - #
# --------------------------------------------------------------------- #
# Ensure database is up before running jobs
is_database_up = False
while not is_database_up:
    is_database_up = True
    try:
        DatabaseInterface.is_database_healthy()
    except:
        print("******************Database not ready********************")
        print("******************Waiting for 5 secs********************")
        is_database_up = False
        time.sleep(5)
        print("******************Try new connection********************")

# Copy targets base to volumes so that workers
# can access it before adding them to the database
src = Config.FOLDER_CONFIG + Config.FILENAME_INIT_TARGETS
dst = Config.FOLDER_UPLOAD + Config.FILENAME_INIT_TARGETS
shutil.copyfile(src, dst)

# Connect to redis and enqueue jobs
redis_server = Redis.from_url(Config.REDIS_URL)
task_queue  = rq.Queue(default_timeout=-1, connection=redis_server)
task_queue.enqueue(DatabaseInterface.targets_update, dst, job_id=Config.REDIS_JOB_ID_INITIALIZE_TARGETS)
task_queue.enqueue(TargetInterface.create_instance_receivesmss, job_id=Config.REDIS_JOB_ID_FETCHER)

# This is the aggressive mode and should not be enabled by default
# task_queue.enqueue(DataInterface.create_data_fetcher, job_id=Config.REDIS_JOB_ID_DATA)

# Configure Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 3600
app.config['UPLOAD_FOLDER'] = Config.FOLDER_UPLOAD







# ---------------------------------------------------------------------- #
# -                            WEB PAGES                               - #
# ---------------------------------------------------------------------- #
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


# ------------------------------------------------------------ #
# -                      SMS ENDPOINT                        - #
# ------------------------------------------------------------ #
@app.route("/search", methods = ['GET'])
def search():
    input_search        = request.args.get('search')
    input_data          = request.args.get('data')
    input_interesting   = request.args.get('interesting')

    if not SecurityInterface.controlerSmsSearch(input_search, input_data, input_interesting):
        abort(403)

    # Get SMSs
    data            = DatabaseInterface.sms_get_by_search(input_search, input_data, input_interesting)
    total_count     = DatabaseInterface.sms_count()
    select_count    = len(data)

    return render_template('search.html', data=data, total_count=total_count, select_count=select_count)

# ---------------------------------------------------------------- #
# -                      AUTOMATION ENDPOINT                     - #
# ---------------------------------------------------------------- #
@app.route("/automation", methods = ['GET'])
def automation():
    # GET INPUTS
    input_search    = request.args.get('search')
    input_legal     = request.args.get('legal')
    input_automated = request.args.get('automated')

    # SECURITY CHECKS
    if not SecurityInterface.controlerAutomationSearch(input_search, input_legal, input_automated):
        abort(403)
    search      = SecurityInterface.controlerReassignString(input_search)
    legal       = SecurityInterface.controlerReassignBoolean(input_legal)
    automated   = SecurityInterface.controlerReassignBoolean(input_automated)

    # Get SMSs
    data    = DatabaseInterface.automation_get_targets(search, legal, automated)
    count   = DatabaseInterface.targets_count()

    return render_template('automation.html', data=data, count=count)

@app.route("/automation/target/update", methods = ['POST'])
def targets_update_automation():
    # Get params
    input_domain        = request.args.get('domain')
    input_is_legal      = request.args.get('is_legal')
    input_is_automated  = request.args.get('is_automated')

    if not SecurityInterface.controlerAutomationUpdate(input_domain, input_is_legal, input_is_automated):
        abort(403)
    is_legal        = SecurityInterface.controlerReassignBoolean(input_is_legal)
    is_automated    = SecurityInterface.controlerReassignBoolean(input_is_automated)
    # domain = SecurityInterface.controlerReassignBoolean(input_domain)

    DatabaseInterface.targets_update_automation(input_domain, is_legal, is_automated)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

# ---------------------------------------------------------------- #
# -                       INVESTIGATION                          - #
# ---------------------------------------------------------------- #
@app.route("/investigation", methods = ['GET'])
def investigation():
    # GET INPUTS
    input_search        = request.args.get('search')
    input_unique        = request.args.get('unique')
    input_unqualified   = request.args.get('unqualified')

    # SECURITY CHECKS
    if not SecurityInterface.controlerInvestigationSearch(input_search, input_unique, input_unqualified):
        abort(403)
    search      = SecurityInterface.controlerReassignString(input_search)
    unique      = SecurityInterface.controlerReassignBoolean(input_unique)
    unqualified = SecurityInterface.controlerReassignBoolean(input_unqualified)

    tags_not_interesting    = Config.LIST_METADATA_INTERESTING_NO
    tags_interesting        = Config.LIST_METADATA_INTERESTING_YES

    # Get SMSs
    data    = DatabaseInterface.sms_get_targets(input_search, input_unique, input_unqualified)
    count   = len(data)

    return render_template('investigation.html', data=data, count=count,
        tags_not_interesting=tags_not_interesting, tags_interesting=tags_interesting)

@app.route("/investigation/target/update", methods = ['POST'])
def targets_update_investigation():
    # Get params
    input_is_interesting  = request.args.get('is_interesting')
    input_domain          = request.args.get('domain')
    input_tags            = request.args.get('tags')

    if not SecurityInterface.controlerInvestigationUpdate(input_is_interesting, input_domain, input_tags):
        abort(403)

    is_interesting  = SecurityInterface.controlerReassignBoolean(input_is_interesting)
    # tags            = SecurityInterface.controlerReassignTags(input_tags)
    # domain          = SecurityInterface.controlerReassignTags(input_domain)

    DatabaseInterface.targets_update_investigation(input_domain, is_interesting, input_tags)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

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
    mode = DatabaseInterface.get_mode()
    return render_template('settings.html', mode=mode)

@app.route("/settings/update_mode", methods = ['POST'])
def settings_update_mode():
    # Wait for 15 seconds to ensure workers exist
    time.sleep(15)

    # Parse inputs
    mode  = request.args.get('mode')
    if not mode in Config.MODES:
        print("In mode list")
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

    current_mode = DatabaseInterface.get_mode()
    print(current_mode)
    print(mode)
    if current_mode == mode:
        print("Same value in database!")
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    

    # Set to passive
    if mode == Config.MODE_AGRESSIVE:
        DatabaseInterface.switch_mode(mode)
        print("Set to aggressive")
        task_queue.enqueue(DataInterface.create_data_fetcher, job_id=Config.REDIS_JOB_ID_DATA)
    # Set to agressive
    if mode == Config.MODE_PASSIVE:
        DatabaseInterface.switch_mode(mode)
        print("Set to passive")
        send_stop_job_command(redis_server, Config.REDIS_JOB_ID_DATA)
        # send_kill_horse_command(redis_server, "data")

    # Check database for current mode
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/settings/export_smss", methods = ['GET'])
def settings_export_smss():
    DatabaseInterface.export_smss()
    return send_file(Config.EXPORT_SMSS, as_attachment=True)

@app.route("/settings/export_targets", methods = ['GET'])
def settings_export_targets():
    DatabaseInterface.export_targets()
    return send_file(Config.EXPORT_TARGETS, as_attachment=True)

@app.route("/settings/export_data", methods = ['GET'])
def settings_export_data():
    DatabaseInterface.export_data()
    return send_file(Config.EXPORT_DATA, as_attachment=True)

@app.route("/settings/export_config", methods = ['GET'])
def settings_export_config():
    DatabaseInterface.export_config()
    return send_file(Config.EXPORT_CONFIG, as_attachment=True)

@app.route("/settings/targets/upload", methods = ['POST'])
def settings_upload_targets():
    file_path = Config.FOLDER_UPLOAD + Config.FILENAME_IMPORT_TARGETS
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(file_path)
        
        DatabaseInterface.targets_update(file_path)  

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    return json.dumps({'success':False}), 400, {'ContentType':'application/json'}


# ----------------------------------------------------------------- #
# -                       ABOUT ENDPOINT                          - #
# ----------------------------------------------------------------- #
@app.route("/about", methods = ['GET'])
def about():
    return render_template('about.html')


# ------------------------------------------------------- #
# -                       DATA                          - #
# ------------------------------------------------------- #
@app.route("/data/get", methods = ['GET'])
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

@app.template_filter('decode')
def decode_msg(encoded):
    decoded = urllib.parse.unquote_plus(encoded)
    decoded = decoded.replace("%26", "&")
    return decoded

# --------------------------------------------------------- #
# -                       ERRORS                          - #
# --------------------------------------------------------- #
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('403.html'), 403