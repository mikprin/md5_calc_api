from test_reqests.recive_hash import *
from test_reqests.send_file import send_file # Send file
from test_reqests.get_hash import get_hash
import argparse, time
import hashlib, random
import numpy as np
from utils_for_test import generate_random_file , calc_hash



def test_heavy(test_url = "http://localhost:8000/")
    parser = argparse.ArgumentParser(description='Set of heavy tests for MD5 api')
    parser.add_argument('--url','--ip', type=str , help="URL or IP of test REST API")
    parser.add_argument('--port', type=str , help="port for the test API")
    args = parser.parse_args()
    if args.url:
        url = args.url
    else:
        url = "localhost"
    if args.port:
        port = args.port
    else:
        port = "8000"
    
    test_url = f"http://{url}:{port}/"
