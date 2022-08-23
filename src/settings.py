### Settings ###

# Import settings from env.
import os,sys
from dotenv import load_dotenv


env_folder = "../.env"
load_dotenv(env_folder)  # take environment variables from .env.

# source_path = os.path.dirname(os.path.realpath(sys.argv[0]))

def get_env_setting(setting):
    if os.getenv(setting):
        return os.getenv(setting)
    else:
        return False


filesystem_work_point = "../appdata"
logdir = "../logs"

# Config envoke here.


# Debug methods can be turned off with DEBUG_API_CALLS = False in main_upload_api.py file (or in general settings if this feature is done)
DEBUG_API_CALLS = get_env_setting("DEBUG_API_CALLS") # 

# Optionally you can save file in chunkes if RAM is limited
CHUNK_SIZE = int(get_env_setting("CHUNK_SIZE"))

# Indicates if extra delay is added for testing on working payload (Default off)
ARTIFITIAL_DELAY = float(get_env_setting("ARTIFITIAL_DELAY")) 



docker_deploy = True # Forgot why it is here

try:
    # celery_filesystem_worker_timeout = int(os.getenv("CELERY_WORKER_FILESYSTEM_TIMEOUT"))
    postgres_credentials = {
        "pguser" : os.getenv("DB_USER"),
        "pgpassword" : os.getenv("DB_PASSWORD"),
        'pghost' : os.getenv("DB_HOST"),
        'pgport' : int(os.getenv("DB_PORT")),
        'pgdb' : os.getenv("DB_NAME")  
    }
except Exception as e:
    print(f"!!!Database Configuration error: {e}.\n Check if database credentials exists in the .env file")
    sys.exit("Database configuration error.  Check if database credentials exists in the .env file.")

