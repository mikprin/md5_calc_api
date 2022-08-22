import numpy as np
import hashlib

def generate_random_file(path,size =1024):
    letters = np.array(list(chr(ord('a') + i) for i in range(26)));
    letters = np.append(letters, '\n' )
    text = np.random.choice(letters, size)
    with open(path, 'w+') as fout:
        fout.write(str(text))

def calc_hash(file_path):
    with open(file_path,'rb') as descriptor:
        hash = hashlib.md5(descriptor.read()).hexdigest()
    return hash