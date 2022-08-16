from fastapi import FastAPI, File, UploadFile # fastapi
from pydantic import BaseModel
import logging,sys # logging

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


@app.get("/")
async def root():
    # print("LOG LOG LOG")
    logging.info(f'Got root request!')
    return {"message": "Hello World"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    logging.info(f'Got file transfer! Fname: {file}')
    return {"filename": file.filename}