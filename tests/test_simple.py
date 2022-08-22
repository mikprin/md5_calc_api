from test_reqests.recive_hash import *
from test_reqests.send_file import send_file # Send file
from test_reqests.get_hash import get_hash
import argparse, time
import hashlib, random
import numpy as np
from utils_for_test import generate_random_file , calc_hash, get_input_arguments

test_file_size = 100
test_file_range = (50,10000)
        

    
    
def test_simple(test_url = "http://localhost:8000/"):
    """Send file and get hash back"""
    test_file_name = "test_file"
    test_passed = 0
    random_file_size = random.randint(*test_file_range)
    generate_random_file(test_file_name, size=random_file_size)

    response = send_file(test_file_name,test_url)
    start = time.time()
    response_content = response.json()
    state = response_content["success"]
    celery_status = response_content["celery_status"]
    if state:
        file_id = response_content["id"]
    else:
        # Send file FAIL here
        print(f"FAIL Failed to send file")

    if celery_status == "PENDING":
        while celery_status == "PENDING":
            response = get_hash(file_id,test_url)
            response_content = response.json()
            celery_status = response_content["status"]
            # print(f"celery_status is {celery_status}")
    else:
        response = get_hash(file_id,test_url)
        response_content = response.json()
        celery_status = response_content["status"]
    if celery_status.upper() == "SUCCESS":
        print(f"Got response! Hash is {response_content['hash']}")
        if response_content["hash"] == calc_hash(test_file_name):
            print(f"Sucsessful and true hash calculation.")
            test_passed = 1
        else:
            print(f"Error in HASH!!!: {response_content['hash']} vs {calc_hash(test_file_name)}")
    else:
        print(f"No success! Status is {response_content['status']}")
    end = time.time()
    print (f"total_time = {end - start}s ")
    assert test_passed == 1
    return test_passed
  
def test_out_of_range_id(test_url = "http://localhost:8000/"):
    '''Test if out of range request is working!'''
    test_passed = 0
    out_of_range_id = 10000
    response = get_hash(out_of_range_id,test_url).json()
    if response["status"] == "INVALID_ID":
        print("INVALID_ID test PASSED")
        test_passed = 1
    assert test_passed == 1
    return test_passed
    
    
    
    
if __name__ == '__main__':
    test_url, args = get_input_arguments()
    test_simple(test_url)
    test_out_of_range_id(test_url)
    sys.exit(0)
    