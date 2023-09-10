import requests
import sys

from config.config import Config
from modules.interface import TargetInterface

# Redis
from redis import Redis
import rq

redis = Redis.from_url(Config.REDIS_URL)
task_queue = rq.Queue(default_timeout=3600, connection=redis)

# Launch workers
task_queue.enqueue(TargetInterface.create_instance_receivesmss)