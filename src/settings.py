### Settings ###

# Import settings from env.
import os
from dotenv import load_dotenv


env_folder = "../.env"
load_dotenv(env_folder)  # take environment variables from .env.

# spurce_path = os.path.dirname(os.path.realpath(sys.argv[0]))

filesystem_work_point = "../appdata"
logdir = "../logs"

save_in_chunkes = False
chunk_size = 2048
# Deployment unsafe development functions
debug_api_calls = True

fake_database = False
# Id range of int values

docker_deploy = True

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
    print(f"!!!Configuration error: {e}")