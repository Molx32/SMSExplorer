import os

SECRET_KEY = 'development'

class Config:
    SITES = [
        "https://receive-smss.com"
    ]

    SEARCH_ENGINES = ["Google", "Bing", "Yahoo", "DuckDuckGo"]

    REDIS_URL       = "redis://"
    REDIS_URL       = "redis://redisserver:6379"
    CELERY_CONFIG={
        'broker_url': 'redis://localhost:6379',
        'result_backend': 'redis://localhost:6379',
    }

class Connections:
    DATABASE = 'postgres'
    USER = 'postgres'
    PASSWORD = 'FileExposer'
    HOST = 'database'
    #HOST = '172.22.0.4'
    #HOST = 'postgres://database'
    #HOST = '172.17.0.2' #127.0.0.1
    PORT='5432'


