# Overview
This is an API develop as a part of Bostongene onboarding contest. Goal was to create a distributed system to send file to API and get hash calculated on the backend with help of celery.

![Overview of the system](./doc/MD5_API_schematic_diagram.png)

# Usage (API reference):
You are free to use API docs `host:8000/docs` to check all by yourself. Or you can use request python scripts to quickly generate the POST requests. Or use them as reference. My text explanation is below:
### To send file
Client (browser or another host) can send HTTP post request containing file. In return, he will get JSON in the form of:
`{ "success" : True/False , "id" : id/None, "celery_status" : status/None , "celery_id" : celery_task_id/none }`
None values correspond to `"success" : False` case.
### To get hash
To get hash, you can use `host:8000/get_hash/{id}` or send ID as request variable: `http://localhost:8000/gethash/?file_id=1`. In return, you get JSON in a form of `{ "status" : status(str) , "hash" : hash(str) }`. In case task is not finished, status will be `'PENDING'`. In case of invalid `id` it should be `"status":'INVALID_ID'`.
### Folder structure

    md5_calc_api
    ├── docs                    # Documentation and task files
    ├── src                     # Source files for API and celery workers. 
    ├── celery                  # 
    ├── docker                  # Docker config files for external pre-build modules (Postgres etc.) 
    ├── tests                   # Automated and not so automated tests
    ├── autoinstall.sh          # Smart install script for Linux
    ├── docker-compose.yml      #  Docker compose file for deploying and building containers
    ├── .env                    #  Important file with environmental variables. autoinstall script can generate it.
    ├── env_example             #  This is a template for `.env` file.
    ├── Dockerfile
    ├── LICENSE
    └── README.md

# Deployment
## Automated
Use `autoinstall.sh` to generate 2 empty folders (volumes) needed by the system and launch docker compose with newly generated `.env` file. I DO NOT save `.env` file in the git repo to prevent passwords leakage.

## Manual
1. `mkdir appdata` Folder for application to store files.
2. `mkdir logs` Folder for logging. Can be altered in docker-compose.yml.
3. `cp env_example .env` To copy the env variables.
4. `docker-compose up -d --build` to deploy.

cd $DIR
docker-compose up -d --build`


## Dependencies
### Linux (any)
Docker (for container managment). You can read about installing docker here: https://docs.docker.com/engine/install/
### Ubuntu
postgresql-devel: (libpq-dev in Debian/Ubuntu, libpq-devel on Centos/Fedora/Cygwin/Babun.). For SQL Alchemy to work.




# Source structure

## src

Main python sources folder. Here are all code including API and celery workers.


    src
    ├── celery_worker.py # Code for celery
    ├── database_tools.py # Tools for SQLAlchemy to create database
    ├── main_upload_api.py # API code with requests
    ├── settings.py # Code to import `.env` variables
    └── templates # HTML templates for the application

## Tests folder
Tests folder consists of a set of tests for the API goal. `simple_test.py` provides low load test to ensure code is working correctly. Organized as unit test. However, giving what this API should prove, I created `load_test.py` which can heavily load the API and backend with set of randomly generated files with pre known hash and throw them at the server counting time to return query of requests. 



# Testing


# Known limitations
* No mechanism to work when parts are distributed behind the proxy server or firewall (mainly to work in local network).
* No security to work in open network. No authorization mechanism.
* File reception of API are limited by filesystem which is common across all the system.
* Not tested in distributed setup
* IDs are not secure numbers. But can be easily made so by using celery worker ID as ID.

# TODO

* `mkdir logs` Folder for logging. Can be altered in docker-compose.yml
* Connection between celery worker results in Postgress and task ID for API database are not related. That ban be fixed easily to enable quicker result search time. However, I'm afraid I don't have time to do it right now.
* Proper catch for out of range ID requests
* Better querys for SQL

# Other
* Full task by task log of development was also posted in my telegram: https://t.me/ee_craft


