from test_reqests.recive_hash import *
from test_reqests.send_file import send_file # Send file
from test_reqests.get_hash import get_hash
import argparse, time
import hashlib, random, os
import numpy as np
from utils_for_test import generate_random_file , calc_hash, get_input_arguments



# def test_heavy(test_url = "http://localhost:8000/", requests_num = 50):
    
    # import shutil
    
    # test_path = "for_tests"
    # os.makedirs(test_path, exist_ok = True)
    
    # # Generate a number of random files
    # test_passed = 0
    # file_list = []
    # hash_list = []
    # file_size_rage = (10,10000)
    # for i in range(requests_num):
    #     file_list.append(i)
    #     generate_random_file(os.path.join(test_path,str(i)), size=random.randint(*file_size_rage))
    #     # hash_list.append(calc_hash(file_list[-1]))

    # # for file in file_list:
    # #     print(f"Process {file}")
    # #     hash_c = calc_hash(file)
    # #     print(hash_c)
    # #     hash_list.append(hash_c)
    
    # shutil.rmtree(test_path)
    # pass

if __name__ == "__main__":
    test_url, args = get_input_arguments()
    # test_heavy()
    