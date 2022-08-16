from dataclasses import dataclass
from re import I
from fastapi import FastAPI, File, UploadFile # fastapi
from pydantic import BaseModel
import logging,sys,os # logging, system
import aiofiles

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

### Settings ###

spurce_path = os.path.dirname(os.path.realpath(sys.argv[0]))
filesystem_work_point = spurce_path


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
async def create_upload_file(incoming_file: UploadFile):
    logging.info(f'Got file transfer! Fname: {incoming_file}')
    # Save complete file in memory
    # Save file in chunks
    return {"id": 1}