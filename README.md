# Overview



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
    ├── Dockerfile
    ├── LICENSE
    └── README.md

# Usage

# Source structure

## Tests
Tests folder consists of set of tests for the API goal. `simple_test.py` provides low load test to enshure code is working correctly. Organized as unit test. However, giving what this API should proof I created `load_test.py` which can heavily load the API and backend with set of randomly generated files with pre known hash and throw them at the server counting time to return query of requests. 

# Build and deployment
## Dependencies

Docker (for container managment). You can read about installing docker here: https://docs.docker.com/engine/install/


### Ubuntu
postgresql-devel: (libpq-dev in Debian/Ubuntu, libpq-devel on Centos/Fedora/Cygwin/Babun.)



# Testing



# TODO

* Database password storage
* Workers and task manager