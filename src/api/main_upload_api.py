# Import config settings
from settings import *


from datetime import datetime

from fastapi import FastAPI, File, UploadFile, Request # fastapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging,sys,os # logging, system
import aiofiles
from threading import Thread
from threading import Lock
import random
import numpy as np

# from dataclasses import dataclass
# from re import I

# For quck file copy?
# import shutil
# from pathlib import Path
# from tempfile import NamedTemporaryFile
# from typing import Callable

if not fake_database:
    # Database imports if used

    # import sqlalchemy as db
    # import sqlalchemy_utils as db_util
    # from sqlalchemy.orm import sessionmaker

    from database_tools import *

#TODO
# Temp measure for importing DB settings
postgres_credentials = {
    "pguser" : 'postgres',
    "pgpassword" : "example",
    'pghost' : "localhost",
    'pgport' : 5432,
    'pgdb' : 'postgres',
}


# Check some additional imports for python < 3.10
if sys.version_info.minor < 10:
    from typing import Union


### Logging ###

logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)



### FastAPI ###

# print("app started")
logging.info("Main script started")
app = FastAPI()

database = {
    1 : {"hash": 1},
    2 : { "hash" : 2 }     
         }

@app.get("/")
async def root():
    # print("LOG LOG LOG")
    logging.info(f'Got root request!')
    return {"message": "Hello World"}

@app.get("/gethash/{file_id}")
async def get_file(file_id: int ):
    ''' Get MD5 from the server back '''
    hash = "12341234"
    # Check that hash exists in the database here
    return hash

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)) :
    logging.info(f'Got incoming file transfer!')
    # Save complete file in memory
    
    # Generate temp filename ( #TODO )
    id = get_new_file_id(database)
    filename = str(id)
    saved_file_path = os.path.join( filesystem_work_point , filename)
    
    
    
    # Simpler way
    # with open(saved_file_path, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)
    
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
    return {"id": id}

if debug_api_calls:
    @app.get("/get-database/")
    async def get_database():
        logging.info(f'Database unload request request!')
        return database

# Static HTML
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

@app.get("/uploadform/", response_class=HTMLResponse)
async def get_upload_form():
    return templates.TemplateResponse("upload_file.html", { "url" : Request.url._url })

### Non API call functions ###

def get_new_file_id(database):
    '''Non locking database ID scan'''
    # ids = np.array( database.keys() ) List version turn out to be faster on more then 1e4 id's
    ids =  database.keys()
    found_id = False
    while not found_id:
        new_id = random.randint(*id_range)
        if not (new_id in ids):
            found_id = True
    return new_id

def add_file_to_database(id:int,filename):
    if fake_database:
        # global database
        database[id] = { "hash" : datetime }
    else:
        #Add file to database for real
        pass
    
