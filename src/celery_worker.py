# from asyncio.log import logger
import logging, os, time
import hashlib, redis
from celery import Celery

from typing import Union
# Import settings from env.
from dotenv import load_dotenv




env_folder = "../.env"
load_dotenv(env_folder)  # take environment variables from .env.

os.environ["CELERY_RESULT_BACKEND"] = f"db+postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
# CELERY_RESULT_BACKEND = 'db+postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:5432/${DB_NAME}'

celery = Celery()
celery.conf.broker_url = os.getenv("CELERY_BROKER_URL")
celery.conf.result_backend = os.getenv("CELERY_BROKER_URL")

# Configure Sherlock's locks to use Redis as the backend,
# never expire locks (actually 120s) and retry acquiring an acquired lock after an
# interval of 0.05 second.
# import sherlock
# from sherlock import RedisLock
# sherlock.configure(expire=None, timeout=20,retry_interval=0.05)


# CELERY_RESULT_BACKEND = 'db+postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:5432/${DB_NAME}'
@celery.task
def md5sum(path,worker_appdata_mount_point = "../appdata", max_timeout = 20, delay_step = 0.5 , log_mutex_name = "log_mutex_new", artificial_delay  : Union[int,bool]  = False ):
    """Worker main function. Calculate hash of the file in `worker_appdata_mount_point` relative to container FS"""
    total_wait_time = 0 # Zero time counter
    
    logfile = "../logs/worker.log" # Logfile hardcoded for now
    
    redis_connection = get_redis_connection()
    # lock = RedisLock(log_mutex_name, client=r) # Now using with
    
    if artificial_delay:
        time.sleep(artificial_delay)

    file_ready = False
    file_path = os.path.join(worker_appdata_mount_point,path)
    logging.info(f"Hashing {file_path}")
    
    # Checking if API is saved file.
    while not file_ready:
        file_ready = os.path.isfile(file_path)
        # logging.info(f"FILE IS READY: {file_ready}")
        if file_ready:
            # Read file and calculate hash
            with open(file_path,'rb') as descriptor:
                hash = hashlib.md5(descriptor.read()).hexdigest()
            logging.info(f"Hash for {file_path} is: {hash}")

            # Log to file using mutex
            if redis_connection: # Check if redis connection exists
                with redis_connection.lock(log_mutex_name):
                    with open(logfile,'a+') as log:
                        log.write(f"\n{file_path} : {hash}")
                # logging.debug(f"lock.locked() == {lock.locked()}")
            else:
                logging.error(f"ERROR: No redis connection for mutex is availible. NO LOGGING IN FILE")
        else:
            # If file is busy
            logging.info(f"Waiting for file  {file_path} to arrive")
            time.sleep(delay_step)
            total_wait_time += delay_step
            if total_wait_time > max_timeout:
                logging.error(f"Worker failed to find file {file_path}")
                return "ERROR"
    if os.getenv("DELETE_FILE").lower() == 'true':
        os.remove(file_path)
    return hash
    
    
def get_redis_connection():
    """Check if redis is ok. Get redis connection"""
    redis_connection = redis.StrictRedis(host=os.getenv("TRUE_REDIS_URL"), port=int(os.getenv("CELERY_BROKER_PORT")), db=2, decode_responses=True)
    try:
        redis_connection.get("test")
    except:
        logging.error("Redis mutexes are not available. REDIS Error")
        locks = False
        return None
    return redis_connection
    