# System
import gevent.monkey
gevent.monkey.patch_all()
import urllib.parse
import time
import json

# Flask
from flask import Flask, abort
from flask import redirect, url_for, request
from flask import render_template
from flask import send_file
from flask import jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

# Redis
import redis
from rq import Queue
from rq.job import Job
from rq import push_connection
from rq import pop_connection
from rq import Connection
from rq.command import send_stop_job_command

# Project - config
from config.config import Config
# Project - interfaces
from modules.source_interface import TargetInterface
from modules.data_interface import DataInterface
from modules.security_interface import SecurityInterface
from database.database import DatabaseInterface
# Project - models
from database.models import User
# Project - tasks
from tasks.tasks import init_database,run_sms_collector

# --------------------------------------------------------------------- #
# -                            START UP                               - #
# --------------------------------------------------------------------- #
# Ensure database is up before running jobs
DatabaseInterface.wait_for_init()
DatabaseInterface.user_create_admin('admin','password123$', 'ADMIN')

# Instanciate app and queue
app = Flask(__name__)
app = Config.init_app(app)
r   = redis.from_url(Config.REDIS_URL)
q   = Queue(connection=r)
# q.enqueue(DatabaseInterface.targets_update, app.config['DST'], job_id=Config.REDIS_JOB_ID_INITIALIZE_TARGETS)
q.enqueue(TargetInterface.create_instance_receivesmss, job_id=Config.REDIS_JOB_ID_FETCHER, job_timeout=-1)

# Configure login
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    infos = DatabaseInterface.user_get(user_id)
    u = User()
    u.id        = str(infos[0])
    u.username  = str(infos[1])
    u.password  = str(infos[2])
    u.role      = str(infos[3])
    return u


# --------------------------------------------------------------------- #
# -                     WEB SERVER GENERIC PAGES                      - #
# --------------------------------------------------------------------- #
# Flask generic pages
@login_manager.unauthorized_handler
def unauthorized():
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_not_authorized(e):
    return render_template('403.html'), 403


# --------------------------------------------------------------------- #
# -                    WEB SERVER PUBLIC PAGES                        - #
# --------------------------------------------------------------------- #
@app.route("/", methods = ['GET','POST'])
@app.route("/explore", methods = ['GET','POST'])
def explore():
    if request.method == 'GET':
        return render_template('explore_search.html')
    if request.method == 'POST':
        pQuery = request.form['query']
        pFilter = request.form['filter']
        # DatabaseInterface.explore()
        return render_template('explore_results.html', query=pQuery, filter=pFilter)
    return render_template('data_search.html')

@app.route("/login", methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        creds = request.json
        username = creds.get('username')
        password = creds.get('password')
        user = DatabaseInterface.user_check(username, password)
        if user:
            u = User()
            u.id        = str(user[0])
            u.username  = str(user[1])
            u.password  = str(user[2])
            u.role      = str(user[3])
            login_user(u)
            return redirect("/home", code=302)
    return render_template('login.html')

# --------------------------------------------------------------------- #
# -                     WEB SERVER ADMIN PAGES                        - #
# --------------------------------------------------------------------- #
@app.route("/home", methods = ['GET'])
@login_required
def home():
    # Get statistics
    count_messages  = DatabaseInterface.sms_count_all()[0]
    count_urls      = DatabaseInterface.sms_count_all_urls()[0]
    count_data      = DatabaseInterface.sms_count_all_data()[0]
    count_unknown   = DatabaseInterface.sms_count_unknown()[0]

    targets_count_known         = DatabaseInterface.targets_count_known()[0]
    targets_count_interesting   = DatabaseInterface.targets_count_interesting()[0]
    targets_count_automated     = DatabaseInterface.targets_count_automated()[0]

    # Activities
    activities_last_data    = DatabaseInterface.sms_activities_last_data()
    top_domains             = DatabaseInterface.sms_activities_top_domains()
    top_errors              = DatabaseInterface.logs_get_errors()

    # Load forms
    return render_template('home.html', active_tab='Home',
        count_messages=count_messages, count_urls=count_urls,
        count_data=count_data, count_unknown=count_unknown,
        targets_count_known=targets_count_known, targets_count_interesting=targets_count_interesting, targets_count_automated=targets_count_automated,
        activities_last_data=activities_last_data, top_domains=top_domains, top_errors=top_errors)

@app.route("/search", methods = ['GET'])
@login_required
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

    return render_template('search.html', active_tab='Search',
        data=data, total_count=total_count, select_count=select_count)

# --- Automation ---- #
@app.route("/automation", methods = ['GET'])
@login_required
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

    return render_template('automation.html', active_tab='Automate',
        data=data, count=count)

@app.route("/automation/target/update", methods = ['POST'])
@login_required
def automation_targets_update():
    # Check if app is locked
    if DatabaseInterface.getLock():
        abort(403)
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

# --- Categorize ---- #
@app.route("/categorize", methods = ['GET'])
@login_required
def categorize():
    # GET INPUTS
    input_search        = request.args.get('search')
    input_unqualified   = request.args.get('unqualified')

    # SECURITY CHECKS
    if not SecurityInterface.controlerCategorizeSearch(input_search, input_unqualified):
        abort(403)
    search      = SecurityInterface.controlerReassignString(input_search)
    unqualified = SecurityInterface.controlerReassignBoolean(input_unqualified)
    print(unqualified)
    tags_not_interesting    = Config.LIST_METADATA_INTERESTING_NO
    tags_interesting        = Config.LIST_METADATA_INTERESTING_YES

    # Get SMSs
    data    = DatabaseInterface.sms_get_targets(search, unqualified)
    count   = len(data)

    return render_template('categorize.html', active_tab='Categorize',
        data=data, count=count,
        tags_not_interesting=tags_not_interesting, tags_interesting=tags_interesting)

@app.route("/categorize/target/update", methods = ['POST'])
@login_required
def categorize_targets_update():
    # Check if app is locked
    if DatabaseInterface.getLock():
        abort(403)
    # Get params
    input_is_interesting  = request.args.get('is_interesting')
    input_domain          = request.args.get('domain')
    input_tags            = request.args.get('tags')

    if not SecurityInterface.controlerCategorizeUpdate(input_is_interesting, input_domain, input_tags):
        abort(403)

    is_interesting  = SecurityInterface.controlerReassignBoolean(input_is_interesting)
    # tags            = SecurityInterface.controlerReassignTags(input_tags)
    # domain          = SecurityInterface.controlerReassignTags(input_domain)

    DatabaseInterface.targets_update_categorize(input_domain, is_interesting, input_tags)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

# --- Statistics ---- #
@app.route("/statistics_telemetry", methods = ['GET'])
@login_required
def statistics_telemetry():
    # GET RAW DATA
    sms_get_count_by_day = DatabaseInterface.sms_get_count_by_day()
    sms_get_count_by_day_labels = [str(row[0]) for row in sms_get_count_by_day]
    sms_get_count_by_day_values = [str(row[1]) for row in sms_get_count_by_day]

    sms_get_top_ten_domains = DatabaseInterface.sms_get_top_ten_domains()
    sms_get_top_ten_domains_labels = [str(row[0]) for row in sms_get_top_ten_domains]
    sms_get_top_ten_domains_values = [str(row[1]) for row in sms_get_top_ten_domains]

    sms_get_top_ten_countries = DatabaseInterface.sms_get_top_ten_countries()
    sms_get_top_ten_countries_labels = [str(row[0]) for row in sms_get_top_ten_countries]
    sms_get_top_ten_countries_values = [str(row[1]) for row in sms_get_top_ten_countries]

    # GET SANITIZED DATA
    san_sms_get_count_by_day = DatabaseInterface.sms_get_count_by_day(sanitized=True)
    san_sms_get_count_by_day_labels = [str(row[0]) for row in san_sms_get_count_by_day]
    san_sms_get_count_by_day_values = [str(row[1]) for row in san_sms_get_count_by_day]

    sms_get_top_ten_domains_unique = DatabaseInterface.sms_get_top_ten_domains_unique(sanitized=True)
    sms_get_top_ten_domains_unique_labels = [str(row[0]) for row in sms_get_top_ten_domains_unique]
    sms_get_top_ten_domains_unique_values = [str(row[1]) for row in sms_get_top_ten_domains_unique]

    sms_get_top_ten_countries_ratio = DatabaseInterface.data_get_top_ten_countries_ratio(sanitized=True)
    sms_get_top_ten_countries_ratio_labels = [str(row[0]) for row in sms_get_top_ten_countries_ratio]
    sms_get_top_ten_countries_ratio_values = [str(row[1]) for row in sms_get_top_ten_countries_ratio]


    return render_template('statistics_telemetry.html', active_tab='Telemetry',
        sms_get_count_by_day_values=sms_get_count_by_day_values, sms_get_count_by_day_labels=sms_get_count_by_day_labels,
        sms_get_top_ten_domains_labels=sms_get_top_ten_domains_labels, sms_get_top_ten_domains_values=sms_get_top_ten_domains_values,
        sms_get_top_ten_countries_labels=sms_get_top_ten_countries_labels, sms_get_top_ten_countries_values=sms_get_top_ten_countries_values,

        san_sms_get_count_by_day_values=san_sms_get_count_by_day_values, san_sms_get_count_by_day_labels=san_sms_get_count_by_day_labels,
        sms_get_top_ten_domains_unique_labels=sms_get_top_ten_domains_unique_labels, sms_get_top_ten_domains_unique_values=sms_get_top_ten_domains_unique_values,
        sms_get_top_ten_countries_ratio_labels=sms_get_top_ten_countries_ratio_labels, sms_get_top_ten_countries_ratio_values=sms_get_top_ten_countries_ratio_values)

@app.route("/statistics_data", methods = ['GET'])
@login_required
def statistics_data():
    # GET SANITIZED DATA
    data_sms_get_count_by_day = DatabaseInterface.data_get_count_by_day(sanitized=True)
    data_sms_get_count_by_day_labels = [str(row[0]) for row in data_sms_get_count_by_day]
    data_sms_get_count_by_day_values = [str(row[1]) for row in data_sms_get_count_by_day]

    data_sms_get_url_count_by_day = DatabaseInterface.data_get_url_count_by_day(sanitized=True)
    data_sms_get_url_count_by_day_labels = [str(row[0]) for row in data_sms_get_url_count_by_day]
    data_sms_get_url_count_by_day_values = [str(row[1]) for row in data_sms_get_url_count_by_day]

    # Get URL per cat - Init
    count_by_category = {}
    for cat in Config.LIST_METADATA_INTERESTING_YES:
        count_by_category[cat] = 0
    for cat in Config.LIST_METADATA_INTERESTING_NO:
        count_by_category[cat] = 0
    # Get URL per cat - Init
    data_get_count_by_category = DatabaseInterface.data_get_count_by_category(sanitized=True)
    for target in data_get_count_by_category:
        count               = target[0]
        # is_interesting      = target[2]
        is_interesting_desc = target[3]
        for cat in Config.LIST_METADATA_INTERESTING_YES + Config.LIST_METADATA_INTERESTING_NO:
            if cat in is_interesting_desc:
                count_by_category[cat] = count_by_category[cat] + count
    count_by_category_labels = list(count_by_category.keys())
    count_by_category_values = list(count_by_category.values())

    data_sms_get_top_ten_domains = DatabaseInterface.data_get_top_ten_domains(sanitized=True)
    data_sms_get_top_ten_domains_labels = [str(row[0]) for row in data_sms_get_top_ten_domains]
    data_sms_get_top_ten_domains_values = [str(row[1]) for row in data_sms_get_top_ten_domains]

    data_sms_get_top_ten_countries = DatabaseInterface.data_get_top_ten_countries(sanitized=True)
    data_sms_get_top_ten_countries_labels = [str(row[0]) for row in data_sms_get_top_ten_countries]
    data_sms_get_top_ten_countries_values = [str(row[1]) for row in data_sms_get_top_ten_countries]

    return render_template('statistics_data.html', active_tab='Data',
        data_sms_get_count_by_day_values=data_sms_get_count_by_day_values, data_sms_get_count_by_day_labels=data_sms_get_count_by_day_labels,
        data_sms_get_url_count_by_day_labels=data_sms_get_url_count_by_day_labels, data_sms_get_url_count_by_day_values=data_sms_get_url_count_by_day_values,
        count_by_category_labels=count_by_category_labels, count_by_category_values=count_by_category_values,
        data_sms_get_top_ten_domains_labels=data_sms_get_top_ten_domains_labels, data_sms_get_top_ten_domains_values=data_sms_get_top_ten_domains_values,
        data_sms_get_top_ten_countries_labels=data_sms_get_top_ten_countries_labels, data_sms_get_top_ten_countries_values=data_sms_get_top_ten_countries_values)

# --- Settings ---- #
@app.route("/settings", methods = ['GET'])
@login_required
def settings():
    mode = DatabaseInterface.get_mode()
    return render_template('settings.html', active_tab='Settings', mode=mode)

@app.route("/settings/update_mode", methods = ['POST'])
@login_required
def settings_update_mode():
    # Check if app is locked
    if DatabaseInterface.getLock():
        abort(403)
    # Wait for 15 seconds to ensure workers exist
    time.sleep(15)

    # Parse inputs
    mode  = request.args.get('mode')
    if not mode in Config.MODES:
        print("In mode list")
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

    current_mode = DatabaseInterface.get_mode()
    if current_mode == mode:
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    # Set to passive
    if mode == Config.MODE_AGRESSIVE:
        DatabaseInterface.switch_mode(mode)
        print("Set to aggressive")
        q.enqueue(DataInterface.create_data_fetcher, job_id=Config.REDIS_JOB_ID_DATA)
    # Set to agressive
    if mode == Config.MODE_PASSIVE:
        DatabaseInterface.switch_mode(mode)
        print("Set to passive")
        send_stop_job_command(r, Config.REDIS_JOB_ID_DATA)
        # send_kill_horse_command(r, "data")

    # Check database for current mode
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/settings/export_smss", methods = ['GET'])
@login_required
def settings_export_smss():
    # Check if app is locked
    if DatabaseInterface.getLock():
        abort(403)
    DatabaseInterface.export_smss()
    return send_file(Config.EXPORT_SMSS, as_attachment=True)

@app.route("/settings/export_targets", methods = ['GET'])
@login_required
def settings_export_targets():
    # Check if app is locked
    if DatabaseInterface.getLock():
        abort(403)
    DatabaseInterface.export_targets()
    return send_file(Config.EXPORT_TARGETS, as_attachment=True)

@app.route("/settings/export_data", methods = ['GET'])
@login_required
def settings_export_data():
    # Check if app is locked
    if DatabaseInterface.getLock():
        abort(403)
    DatabaseInterface.export_data()
    return send_file(Config.EXPORT_DATA, as_attachment=True)

@app.route("/settings/export_config", methods = ['GET'])
@login_required
def settings_export_config():
    # Check if app is locked
    if DatabaseInterface.getLock():
        abort(403)
    DatabaseInterface.export_config()
    return send_file(Config.EXPORT_CONFIG, as_attachment=True)

@app.route("/settings/targets/upload", methods = ['POST'])
@login_required
def settings_upload_targets():
    # Check if app is locked
    if DatabaseInterface.getLock():
        abort(403)
    file_path = Config.FOLDER_UPLOAD + Config.FILENAME_IMPORT_TARGETS
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(file_path)
        
        DatabaseInterface.targets_update(file_path)

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

@app.route("/settings/lock", methods = ['POST'])
@login_required
def settings_lock_app():
    # Check if app is locked
    if DatabaseInterface.getLock():
        abort(403)
    DatabaseInterface.setLock()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/settings/audit_logs", methods = ['GET'])
@login_required
def audit_logs():
    # Get params
    input_search    = request.args.get('search')
    input_start     = request.args.get('start')
    input_end       = request.args.get('end')

    if not SecurityInterface.controlerAuditLogsSearch(input_search, input_start, input_end):
        abort(403)
    input_search    = SecurityInterface.controlerReassignString(input_search)
    start, end      = SecurityInterface.controlerReassignDbStartEnd(input_start, input_end)

    # Get data
    audit_logs = DatabaseInterface.get_audit_logs(input_search, input_start, input_end)
    
    # Calculate previous and next pages
    prev_start  = max(start - 50, 0)
    prev_end    = prev_start + 50
    next_start  = start + 50
    next_end    = next_start + 50

    return render_template('audit_logs.html', active_tab='AuditLogs',
        input_search=input_search, data=audit_logs,
        start=start, end=end,
        prev_start=prev_start, prev_end=prev_end,
        next_start=next_start, next_end=next_end)

@app.route("/settings/about", methods = ['GET'])
@login_required
def about():
    supported_targets = DatabaseInterface.sms_get_supported_targets()
    return render_template('about.html', active_tab='About', targets=supported_targets)

@app.route("/settings/monitor", methods = ['GET'])
@login_required
def monitor():
    job_ids = [
        Config.REDIS_JOB_ID_INITIALIZE_TARGETS,
        Config.REDIS_JOB_ID_DATA,
        Config.REDIS_JOB_ID_FETCHER
    ]
    jobs = Job.fetch_many(job_ids, connection=r)
    jobs_info = []
    for job in jobs:
        if job:
            info = (
                job.get_status(),
                job.worker_name,
                job.last_heartbeat,
                job.started_at
            )
            jobs_info.append(info)

    return render_template('monitor.html', active_tab='Monitor', jobs=jobs_info)

# --- Logout ---- #
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/explore')

# --- Settings ---- #
@app.route("/data/get", methods = ['GET'])
@login_required
def data():

    # Get searched SMSs
    if request.args.get('id'):
        sms_id = request.args.get('id')
        data = DatabaseInterface.sms_get_data_by_id(sms_id)[0]
    # Get all SMSs
    else:
        data = {}
    return jsonify(data)

@app.template_filter('decode')
def decode_msg(encoded):
    decoded = urllib.parse.unquote_plus(encoded)
    decoded = decoded.replace("%26", "&")
    return decoded


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)