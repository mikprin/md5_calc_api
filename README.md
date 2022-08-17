# Overview



### Folder structure

    .
    ├── build                   # Compiled files
    ├── docs                    # Documentation and task files
    ├── src                     # Source files for API. Including docker build scripts
    ├── docker                  # Docker config files for external pre build modules (postgres etc) 
    ├── tests                   # Automated and not so automated tests
    ├── tools                   # Tools and utilities
    ├── autoinstall.sh          # Smart install script for linux
    ├── LICENSE
    └── README.md

# Usage

# Source structure

## Tests
Tests folder consists of set of tests for the API goal. `simple_test.py` provides low load test to enshure code is working correctly. Organized as unit test. However, giving what this API should proof I created `load_test.py` which can heavily load the API and backend with set of randomly generated files with pre known hash and throw them at the server counting time to return query of requests. 

# Build and deployment
## Dependencies
### Ubuntu
postgresql-devel: (libpq-dev in Debian/Ubuntu, libpq-devel on Centos/Fedora/Cygwin/Babun.)



# Testing



# TODO

* Database password storage
* Workers and task manager