# System
import requests
import sys
from datetime import datetime
import time

from config.config import Config
from modules.interface import TargetInterface

# Database
from database.database import DatabaseInterface

# Temp
from database.models import SMS

# Flask
from flask import Flask
from flask import redirect, url_for, request
from flask import render_template
from flask import render_template_string
from forms.forms import SearchForm
import urllib.parse


# Redis
from redis import Redis
import rq
from rq.worker import Worker, WorkerStatus
from rq.command import send_kill_horse_command

redis = Redis.from_url(Config.REDIS_URL)
task_queue = rq.Queue(default_timeout=3600, connection=redis)

# sms = SMS()
# d = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
# sms.setAttribute('receive_date', d)
# sms.setAttribute('sender', 'mySender')
# sms.setAttribute('receiver', 'myReceiver')
# sms.setAttribute('msg', 'thisIsASuperMessage')

# data = DatabaseInterface.sms_insert(sms)
# data = DatabaseInterface.sms_get_by_search("facebook")
# for d in data:
#     print(d)

# Launch workers
task_queue.enqueue(TargetInterface.create_instance_receivesmss)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'totomakey'
# Launch Flask
# -----------------------------------------------------------------#
# SEARCH ENDPOINT
    
@app.route("/")
@app.route("/search", methods = ['GET'])
def default():
    form = SearchForm()
    count = DatabaseInterface.sms_count()
    if request.args.get('search'):
        search = request.args.get('search')
        data = DatabaseInterface.sms_get_by_search(search)
    else:
        data = DatabaseInterface.sms_get_all()

    return render_template('search.html', form=form, data=data, count=count)


@app.route("/clean", methods = ['GET'])
def clean():
    workers = Worker.all(redis)
    for worker in workers:
        send_kill_horse_command(redis, worker.name)
    time.sleep(5)
    DatabaseInterface.clean_database()
    # Relaunch workers
    task_queue.enqueue(TargetInterface.create_instance_receivesmss)
    return redirect('/search')


@app.template_filter('decode')
def decode_msg(encoded):
    decoded = urllib.parse.unquote_plus(encoded)
    decoded = decoded.replace("%26", "&")
    return decoded


