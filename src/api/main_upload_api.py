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


@app.get("/")
async def root():
    # print("LOG LOG LOG")
    logging.info(f'Got root request!')
    return {"message": "Hello World"}

@app.post("/uploadfile/")
async def create_upload_file(incoming_file: UploadFile):
    logging.info(f'Got file transfer! Fname: {incoming_file}')
    # Save complete file in memory
    async with aiofiles.open(saved_file_path, "wb") as saved_file:
        content_of_file = await incoming_file.read()
        await saved_file.write(content_of_file)

    # Save file in chunks
    return {"id": 1}