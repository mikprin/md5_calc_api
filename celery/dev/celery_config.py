CELERY_IMPORTS = ("tasks")
CELERY_IGNORE_RESULT = False
BROKER_HOST = "127.0.0.1"
BROKER_PORT = 5672
BROKER_URL = "amqp://"

from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    
}