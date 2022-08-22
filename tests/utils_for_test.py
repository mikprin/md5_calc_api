import numpy as np
import hashlib


def get_input_arguments():
    '''Get CLI arguments for tests'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Set tests for MD5 api')
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
    return test_url,args

def generate_random_file(path,size =1024):
    letters = np.array(list(chr(ord('a') + i) for i in range(26)))
    letters = np.append(letters, '\n' )
    text = np.random.choice(letters, size)
    with open(path, 'w+') as fout:
        fout.write(str(text))

def calc_hash(file_path):
    with open(file_path,'rb') as descriptor:
        hash = hashlib.md5(descriptor.read()).hexdigest()
    return hash