# Overview
![Overview of the system]([http://url/to/img.png](https://github.com/mikprin/md5_calc_api/blob/master/doc/MD5_API_schematic_diagram.png))


### Folder structure

    .
    ├── docs                    # Documentation and task files
    ├── src                     # Source files for API and celery workers. 
    ├── celery                  # 
    ├── docker                  # Docker config files for external pre build modules (postgres etc) 
    ├── tests                   # Automated and not so automated tests
    ├── autoinstall.sh          # Smart install script for linux
    ├── docker-compose.yml      #  Docker compose file for deploying and building containers
    ├── .env                    #  Important file with enviormental variables. autoinstall script can generate it.
    ├── env_example             #  This is a template for `.env` file.
    ├── Dockerfile
    ├── LICENSE
    └── README.md


# Deployment
## Automated
Use `autoinstall.sh` to generate 2 empty folders needed by the system and launch docker compose with newly generated `.env` file. I DO NOT save `.env` file in the git repo to prevent passwords leakage.

## Manual
1. `mkdir appdata` Folder for application to store files.
2. `mkdir logs` Folder for logging. Can be altered in docker-compose.yml.
3. `cp env_example .env` To copy the env variables.
4. `docker-compose up -d --build` to deploy.

cd $DIR
docker-compose up -d --build`
# Usage

# Source structure

## Tests
Tests folder consists of set of tests for the API goal. `simple_test.py` provides low load test to enshure code is working correctly. Organized as unit test. However, giving what this API should proof I created `load_test.py` which can heavily load the API and backend with set of randomly generated files with pre known hash and throw them at the server counting time to return query of requests. 

# Build and deployment
## Dependencies

Docker (for container managment). You can read about installing docker here: https://docs.docker.com/engine/install/


### Ubuntu
postgresql-devel: (libpq-dev in Debian/Ubuntu, libpq-devel on Centos/Fedora/Cygwin/Babun.). For SQLAlchemy to work.



# Testing


# Known limitations
* No mechanism to work when parts are distributed behind the proxy server or firewall (mainly to work in local network).
* File reception of API are limited by filesystem which is common across all the system.

# TODO

`mkdir logs` Folder for logging. Can be altered in docker-compose.yml