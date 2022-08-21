# from this import s
from urllib import response
from test_reqests.recive_hash import *
from test_reqests.send_file import send_file # Send file
from test_reqests.get_hash import get_hash
import argparse, time

test_file_size = 1024
        
        
def generate_random_file(path,size):
    with open(path, 'wb') as fout:
        fout.write(os.urandom(size))

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

    test_file_name = "test_file"
    generate_random_file(test_file_name,test_file_size)
    
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
            response = get_hash(test_file_name,test_url)
            response_content = response.json()
            state = response_content["status"]
    else:
        response = get_hash(test_file_name,test_url)
        response_content = response.json()
        state = response_content["status"]
    if state == "success":
        print(f"Test passed! Hash is {response_content['hash']}")
    else:
        print(f"No success! Status is {response_content['status']}")
    end = time.time()
    print (f"total_time = {end - start}s ")
    # if response
    # get_hash