from importlib.metadata import files
import requests
import os, sys

test_url = "http://127.0.0.1:8000/"
test_port = 8000


test_script_path = os.path.dirname(os.path.realpath(sys.argv[0]))

test_file_name = "test_file"

test_file_path = os.path.join( test_script_path , test_file_name)


def get_hash(id,test_url = "http://127.0.0.1:8000/"):
    # test_file = open("test_file", "rb")
    
    request_url = os.path.join( test_url, "gethash")

    test_response = requests.get(request_url, data={"file_id": id} )

    # test_response = requests.post(test_url, files = {"form_field_name": test_file})
    if test_response.ok:
        print("Hash request completed successfully!")
        print(test_response.text)
    else:
        print(f"Hash request went wrong! Answer: {test_response.text}")
    return test_response

if __name__ == '__main__':
    id = 1
    get_hash(id)