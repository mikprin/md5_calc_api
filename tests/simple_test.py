# from this import s
from urllib import response
from test_reqests.recive_hash import *
from test_reqests.send_file import send_file # Send file
from test_reqests.get_hash import get_hash
import argparse, time
import hashlib, random
import numpy as np

test_file_size = 100
test_file_range = (50,10000)
        
def generate_random_file(path,size =1024):
    
    # n = size ** 2  # 1 Mb of text
    letters = np.array(list(chr(ord('a') + i) for i in range(26)));
    letters = np.append(letters, '\n' )
    text = np.random.choice(letters, size)
    # print(text)
    
    with open(path, 'w+') as fout:
        fout.write(str(text))
    # np.savetxt(path,text, delimiter='')
    
def calc_hash(file_path):
    with open(file_path,'rb') as descriptor:
        hash = hashlib.md5(descriptor.read()).hexdigest()
    return hash
    
    
def commit_simple_test(test_url):
    test_file_name = "test_file"
    test_passed = 0
    random_file_size = random.randint(*test_file_range)
    generate_random_file(test_file_name, size=random_file_size)
    
    # send_time = 
    
    
    response = send_file(test_file_name,test_url)
    start = time.time()
    response_content = response.json()
    state = response_content["success"]
    if state:
        file_id = response_content["id"]
    else:
        # Send file FAIL here
        pass

    if state == "PENDING":
        while state == "PENDING":
            response = get_hash(file_id,test_url)
            response_content = response.json()
            state = response_content["status"]
    else:
        response = get_hash(file_id,test_url)
        response_content = response.json()
        state = response_content["status"]
    if state.upper() == "SUCCESS":
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

    return test_passed
    
    
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
    
    test_url = f"http://{url}:{port}/"
    commit_simple_test(test_url)
    