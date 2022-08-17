from test_reqests.recive_hash import *
from test_reqests.send_file import * # Send file

import argparse

if __name__ == '__main__':
    
    
    parser = argparse.ArgumentParser(description='Set of tests for MD5 api')
    
    parser.add_argument('--url','--ip', type=str , help="URL or IP of test REST API")
    parser.add_argument('--port', type=str , help="URL or IP of test API")
    args = parser.parse_args()
    if args.url:
        url = args.url
    else:
        url = "localhost"
    if args.port:
        port = args.port
    else:
        port = "8000"
    
        
        
def generate_random_file(path,size):
    with open("path", 'wb') as fout:
        fout.write(os.urandom(size))
    
