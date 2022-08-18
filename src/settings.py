### Settings ###

# spurce_path = os.path.dirname(os.path.realpath(sys.argv[0]))

filesystem_work_point = "../appdata"

save_in_chunkes = False
chunk_size = 2048
# Deployment unsafe development functions
debug_api_calls = True

fake_database = False

# Id range of int values
id_range = (1,int(1e1))

docker_deploy = True

# Database credentials
if docker_deploy:
    postgres_credentials = {
        "pguser" : 'postgres',
        "pgpassword" : "example",
        'pghost' : "host.docker.internal",
        'pgport' : 5432,
        'pgdb' : 'md5hashes',
    }
else:
    postgres_credentials = {
        "pguser" : 'postgres',
        "pgpassword" : "example",
        'pghost' : "localhost",
        'pgport' : 5432,
        'pgdb' : 'md5hashes',
    }