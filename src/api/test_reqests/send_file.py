import requests
import os, sys

test_url = "http://127.0.0.1:8000/uploadfile/"
test_port = 8000


test_script_path = os.path.dirname(os.path.realpath(sys.argv[0]))

test_file_name = "test_file"

test_file_path = os.path.join( test_script_path , test_file_name)

# test_file = open("test_file", "rb")
with open(test_file_path) as test_file:
    test_response = requests.post(test_url, data={'filename': test_file , "msg":"hello" ,"type" : "multipart/form-data"}, files = { "file" : test_file  } )

# test_response = requests.post(test_url, files = {"form_field_name": test_file})

if test_response.ok:
    print("Upload completed successfully!")
    print(test_response.text)
else:
    print(f"Something went wrong! Answer: {test_response.text}")