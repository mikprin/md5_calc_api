'''Man source for FastAPI code for distributed MD5 calculation'''

# Standard imports
import os
import logging,sys,os, glob, pathlib, time # logging, system
import aiofiles

from fastapi import FastAPI, File, UploadFile, Request, Body # fastapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import config settings
from settings import *

# Worker import
from celery_worker import  md5sum
from celery import Celery
from celery.result import AsyncResult
os.environ["CELERY_RESULT_BACKEND"] = f"db+postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
# Celery init
celery = Celery()
celery.conf.broker_url = os.getenv("CELERY_BROKER_URL")
celery.conf.result_backend = os.getenv("CELERY_BROKER_URL")


### Logging setup ###
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

logging.info("Main script started")
# root_path = os.path.realpath(__file__)
root_path = pathlib.Path(__file__).parent.resolve()
current_dir = pathlib.Path().resolve()
logging.info(f"Working dir: {current_dir}")

# There are two options for database: real one and a temp one in memory


logging.info("Using postgres database. Trying to connect")
from database_tools import *

### Initiage database (using database tools) ###
try:
    database_sesstion,database_engine = get_session(postgres_credentials)
except:
    logging.error("""Failed to open database. Terminating. Possible solutions are:
                    check database container is running, check credentials (password, URL and user).
                    Check networking and port availability from your machine!
                """)
    sys.exit("Database connection error.")
database = API_database(database_sesstion,database_engine)


# Create directory if needed:
os.makedirs(os.path.join(root_path,"static"), exist_ok=True) # For static HTML after templating
os.makedirs(filesystem_work_point, exist_ok=True) # Where files saved in container



### FastAPI ###

app = FastAPI()
# Static HTML

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    ''' Root welcome JSON '''
    # print("LOG LOG LOG")
    logging.info(f'Got root request!')
    return {"message": "Welcome you on my BG task submission API"}

@app.get("/gethash/")
async def get_file_hash(file_id: int ):
    ''' Get MD5 from the server back. fild ID as input hash as output. '''
    logging.info(f"Getting hash for {file_id}")
    # print(f"Getting hash for {file_id}")
    result = await get_hash_result(file_id, database)
    # result = 1
    # Check that hash exists in the database here
    return result

@app.get("/gethash/{file_id}")
async def get_file_hash_from_url(file_id: int , request: Request):
    ''' Get MD5 from the server back but pass URL as ID '''
    logging.info(f"Getting hash for {file_id}")
    result = await get_hash_result(file_id, database)
    return result

@app.get("/gethash-form/")
async def get_file_hash_from_url(file_id: int , request: Request ):
    ''' Get MD5 from the server back but get HTML in return'''
    logging.info(f"Getting hash for {file_id}")
    result = await get_hash_result(file_id, database)
    if result["status"] == "SUCCESS":
        return templates.TemplateResponse("return_hash.html", { "hash": result["hash"] ,  "request": request  })
    elif result["status"] == "PENDING":
        pass
        # PENDING HTML
        # return templates.TemplateResponse("return_hash.html", { "hash": result["hash"] ,  "request": request  })
    else:
        return templates.TemplateResponse("return_hash_error.html", { "status": result["status"] , "request": request  })
    
@app.post("/uploadfile/")
async def create_upload_file(request: Request ,  file: UploadFile = File(...)) :
    ''' Upload file and get ID of the file back. If request.source = "HTML" then get HTML with ID '''
    logging.info(f"Incoming request: {request.body()}")
    logging.info(f'Got incoming file transfer!')
    id = database.get_new_id()
    filename = str(id)
    result = await save_and_start_hashing(file,database) # LAUNCHING WORKER HERE
    return result

@app.post("/uploadfile-html/")
async def create_upload_file_html(request: Request, source: str = "api" ,  file: UploadFile = File(...)) :
    ''' Upload file and get ID of the file back. If request.source = "HTML" then get HTML with ID '''
    logging.info(f"Incoming request: {request.body()}")
    logging.info(f'Got incoming file transfer from HTML page!')
    result = await save_and_start_hashing(file,database)
    if result["success"]:
        return templates.TemplateResponse("return_id.html", { "request": request , "id": result["id"] })
    else:
        return templates.TemplateResponse("return_error.html", { "request": request , "id": "FAILED" })

if DEBUG_API_CALLS:
    @app.get("/get-database/")
    async def get_database():
        '''Debug call to return the database. This and other debug methods can be turned off with DEBUG_API_CALLS = False in main_upload_api.py file (or in general settings if this feature is done).'''
        logging.info(f'Database unload request!')
        #TODO return database here
        return "Your database will be here!"
    
    @app.post("/cleardatabase/")
    async def clear_database():
        '''Debug call to clear all database and delete all local files exept logs. This and other debug methods can be turned off with DEBUG_API_CALLS = False in main_upload_api.py file (or in general settings if this feature is done).'''
        logging.info(f'Deleting database!')
        database.drop_all_files()    
        logging.info(f'Deleting files!')
        files = glob.glob(os.path.join(filesystem_work_point,"*"))
        for f in files:
            os.remove(f)
        return { "status" : "success" }

    @app.get("/error/")
    async def return_error_html(request: Request):
        '''Debug call to get to error page to demonstrate it if no errors occur on the demo. This and other debug methods can be turned off with DEBUG_API_CALLS = False in main_upload_api.py file (or in general settings if this feature is done).'''
        return templates.TemplateResponse("return_error.html", { "request": request })


@app.get("/uploadform/", response_class=HTMLResponse)
async def get_upload_form(request: Request):
    '''Static HTML app to Upload file and get ID of the file back.'''
    return templates.TemplateResponse("upload_file.html", { "request": request })



### Non API async call functions ###

async def save_and_start_hashing(file, database):
    """In this function I save the file and call the celery worker. Get Worker ID and add it to database"""
    id = database.get_new_id()
    filename = str(id)
    if database.add_file_to_quene(id, filename):
        saved_file_path = os.path.join( filesystem_work_point , filename)
        await save_file(file,saved_file_path)
        
        worker = md5sum.delay(filename,artificial_delay = ARTIFITIAL_DELAY )
        database.add_worker_id(id,worker.id)
        return{ "success" : True , "id" : id, "celery_status" : worker.status, "celery_id" : worker.id }
    else:
        logger.error("Failed to add {id} to database")
        return {"id": None, "success": False , "id" : None, "celery_status" : None, "celery_id" : None }


async def save_file(file, saved_file_path):
    if CHUNK_SIZE:
        # Save file in chunks
        async with aiofiles.open(saved_file_path, 'wb') as saved_file:
            while content_of_file := await file.read(CHUNK_SIZE):  # async read chunk
                await saved_file.write(content_of_file)  # async write chunk
    else:
        # Save file in one piece
        async with aiofiles.open(saved_file_path, "wb") as saved_file:
            content_of_file = await file.read()
            await saved_file.write(content_of_file)
    logging.info(f"File saved as: {saved_file_path}")
    

async def get_hash_result(file_id,database):
    task_id = database.get_worker_id(file_id)
    if not task_id:
        return {"status" : "INVALID_ID" , "hash" : None }
    res = AsyncResult(task_id)
    if res.status != ("SUCCESS" or "PENDING"):
        logging.error(f"Status of {file_id} with task {task_id} is {res.status}")
    return {"status" : res.status , "hash" : res.result }
