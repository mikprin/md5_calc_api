# Import config settings
import os
from settings import *


from datetime import datetime

from fastapi import FastAPI, File, UploadFile, Request, Body # fastapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging,sys,os, glob, pathlib, json, time # logging, system
import aiofiles
from threading import Thread
from threading import Lock
import random, pickle
import numpy as np

from celery_worker import  md5sum

### Logging setup ###

logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

logging.info("Main script started")
# root_path = os.path.realpath(__file__)
root_path = pathlib.Path(__file__).parent.resolve()
current_dir = pathlib.Path().resolve()
logging.info(f"Working dir: {current_dir}")


# There are two options for database: real one and a temp one in memory

# Database imports if used
logging.info("Using real database. Trying to connect")
# import sqlalchemy as db
# import sqlalchemy_utils as db_util
# from sqlalchemy.orm import sessionmaker
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
    
#TODO
# Temp measure for importing DB settings


# Check some additional imports for python < 3.10
if sys.version_info.minor < 10:
    from typing import Union

# Create directory if needed:
os.makedirs(os.path.join(root_path,"static"), exist_ok=True)
os.makedirs(filesystem_work_point, exist_ok=True)



### FastAPI ###

app = FastAPI()


@app.get("/")
async def root():
    # print("LOG LOG LOG")
    logging.info(f'Got root request!')
    return {"message": "Welcome you on my BG task submission API"}

@app.get("/gethash/")
async def get_file_hash(file_id: int ):
    ''' Get MD5 from the server back '''
    result = get_hash_from_database(file_id, database)
    # Check that hash exists in the database here
    return result

@app.get("/gethash/{file_id}")
async def get_file_hash_from_url(file_id: int ):
    ''' Get MD5 from the server back but pass URL as ID '''
    result = get_hash_from_database(file_id, database)
    # Check that hash exists in the database here
    return result

@app.post("/uploadfile/")
async def create_upload_file(request: Request ,  file: UploadFile = File(...)) :
    ''' Upload file and get ID of the file back. If request.source = "HTML" then get HTML with ID '''
    logging.info(f"Incoming request: {request.body()}")
    logging.info(f'Got incoming file transfer!')

    # Save complete file in memory
    # Generate temp filename ( #TODO )
    id = database.get_new_id()
    filename = str(id)
    result = await save_and_start_hashing(file,database) # LAUNCHING WORKER HERE
    return result

@app.post("/uploadfile-html/")
async def create_upload_file(request: Request, source: str = "api" ,  file: UploadFile = File(...)) :
    ''' Upload file and get ID of the file back. If request.source = "HTML" then get HTML with ID '''
    logging.info(f"Incoming request: {request.body()}")
    logging.info(f'Got incoming file transfer from HTML page!')
    result = await save_and_start_hashing(file,database)
    if result["success"]:
        return templates.TemplateResponse("return_id.html", { "request": request , "id": result["id"] })
    else:
        return templates.TemplateResponse("return_id.html", { "request": request , "id": "FAILED" })

if debug_api_calls:
    @app.get("/get-database/")
    async def get_database():
        '''Debug call to return the database. Debug methods can be turned off with debug_api_calls = False'''
        logging.info(f'Database unload request request!')
        return database #TODO return database here
    
    @app.post("/cleardatabase/")
    async def clear_database():
        '''Debug call to clear all database. Debug methods can be turned off with debug_api_calls = False'''
        logging.info(f'Deleting database!')
        database.drop_all_files()    
        logging.info(f'Deleting files!')
        files = glob.glob(os.path.join(filesystem_work_point,"*"))
        for f in files:
            os.remove(f)
        return { "status" : "success" }


# Static HTML

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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
        worker = md5sum.delay(filename)
        database.add_worker_id(id,worker.id)
        return{ "success" : True , "id" : id, "celery_status" : worker.status, "celery_id" : worker.id }
    else:
        logger.error("Failed to add {id} to database")
        return {"id": None, "success": False , "id" : None, "celery_status" : None, "celery_id" : None }


async def save_file(file, saved_file_path):
    if save_in_chunkes:
        # Save file in chunks
        async with aiofiles.open(saved_file_path, 'wb') as saved_file:
            while content_of_file := await file.read(chunk_size):  # async read chunk
                await saved_file.write(content_of_file)  # async write chunk
    else:
        # Save file in one piece
        async with aiofiles.open(saved_file_path, "wb") as saved_file:
            content_of_file = await file.read()
            await saved_file.write(content_of_file)
    logging.info(f"File saved as: {saved_file_path}")
    
def get_hash_from_database(file_id,database):
    try:
        result = database.get_hashing_results(file_id)
    except Exception as err:
        logging.error(f"When database.get_hashing_results error: with database. Error description: {e}")
        result = { "status" : "DATABASE_FAIL" , "hash" : None }