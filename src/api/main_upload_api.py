# Import config settings
from settings import *


from datetime import datetime

from fastapi import FastAPI, File, UploadFile, Request, Body # fastapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging,sys,os, pathlib, json, time # logging, system
import aiofiles
from threading import Thread
from threading import Lock
import random
import numpy as np

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
if not fake_database:
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
                      check database container is running, check credentials (password and user).
                      Also it is possible to set `fake_database = True` as a config variable to use temperary database in memory""")
        pass

#TODO
# Temp measure for importing DB settings


# Check some additional imports for python < 3.10
if sys.version_info.minor < 10:
    from typing import Union

# Create directory if needed:

# mkdir working dirs if not exist

os.makedirs(os.path.join(root_path,"static"), exist_ok=True)
os.makedirs(filesystem_work_point, exist_ok=True)



### FastAPI ###

app = FastAPI()

# Temp database created
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

@app.get("/gethash/")
async def get_file(file_id: int ):
    ''' Get MD5 from the server back '''
    hash = "12341234"
    # Check that hash exists in the database here
    return hash

@app.post("/uploadfile/")
async def create_upload_file(request: Request, file: UploadFile = File(...)) :
    logging.info(f"Incoming request: {request.body()}")
    logging.info(f'Got incoming file transfer!')
    # print("++++++++++")
    # json_formatted_str = json.dumps(request.json(), indent=2)
    # print(json_formatted_str)
    # print("++++++++++")
    # if request.source

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
    # return request.json()

if debug_api_calls:
    @app.get("/get-database/")
    async def get_database():
        logging.info(f'Database unload request request!')
        return database

# Static HTML

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/uploadform/", response_class=HTMLResponse)
async def get_upload_form(request: Request):
    return templates.TemplateResponse("upload_file.html", { "request": request })

@app.get("/showid", response_class=HTMLResponse)
async def get_upload_form(request: Request):
    return templates.TemplateResponse("showid.html", { "request": request })


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
    
