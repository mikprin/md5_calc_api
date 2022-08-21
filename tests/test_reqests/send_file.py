# from importlib.metadata import files
# from wsgiref.util import request_uri
import requests
import os, sys
import numpy as np


test_port = 8000
test_url = "http://127.0.0.1:8000/"



test_script_path = os.path.dirname(os.path.realpath(sys.argv[0]))



test_file_name = "test_file"
test_file_path = os.path.join( test_script_path , test_file_name)
size = 20

letters = np.array(list(chr(ord('a') + i) for i in range(26)));
letters = np.append(letters, '\n' )
text = np.random.choice(letters, size)
# print(text)
    
with open(test_file_name, 'w+') as fout:
    fout.write(str(text))




def send_file(test_file_path,test_url):
    # test_file = open("test_file", "rb")

    request_url = os.path.join( test_url, "uploadfile")
    with open(test_file_path) as test_file:
        # test_response = requests.post(test_url, data={'filename': test_file , "msg":"hello" ,"type" : "multipart/form-data"}, files = { "file" : test_file  } )
        test_response = requests.post(request_url, data={
            'filename': test_file_name , "msg":"hello" ,"type" : "multipart/form-data" , 'Content-Type': "multipart/form-data"}, files = { "file" : test_file} )

    # test_response = requests.post(test_url, files = {"form_field_name": test_file})

    if test_response.ok:
        print("Upload completed successfully!")
        print(test_response.text)
    else:
        print(f"Something went wrong! Answer: {test_response.text}")
    # return test_response.status_code
    return test_response

if __name__ == '__main__':
    send_file(test_file_path,test_url)