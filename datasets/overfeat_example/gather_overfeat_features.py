#!/Users/wonderland/anaconda3/bin/python3

import io
import subprocess
import os
from collections import defaultdict
import hashlib
import sys

import numpy as np

def gather_files(datadirectory, exclude=None):

    class_to_filename = defaultdict(list)
    
    
    for dirpath, dirs, files in os.walk(datadirectory):
        for filename in files:

            classname = os.path.basename(dirpath)
            file_location = os.path.join(dirpath,filename)
            class_to_filename[classname].append(file_location)
    return class_to_filename


def get_matrix_row_n(class_to_file):
    rows = sum(map(len, class_to_file.values()))
    return rows

def overfeat_feature_n():
    return 4096


def create_overfeat_argument_list(class_to_filename):

    X = []
    y = []
    
    for class_n, input_list in class_to_filename.items():

        for input_k in input_list:
            X.append(input_k)
            y.append(class_n)


    return X, y
        

def divide_chunks(l, n):
    for i in range(0, len(l), n): 
        yield l[i:i + n]




def run_overfeat(overfeat_input, n_rows, n_cols):
    chunk_size = 5000
    X = np.empty((n_rows, n_cols), dtype=np.float)
    line_number = 0
    for k, input_argument in enumerate(divide_chunks(overfeat_input, chunk_size)):


        commandline_input = " ".join(input_argument)
        #print(commandline_input)
    
        proc = subprocess.Popen([overfeat_binary, overfeat_options, commandline_input], stdout=subprocess.PIPE)
        for line in io.TextIOWrapper(proc.stdout):         
            if line_number % 2 == 1:
                x = np.fromstring(line, dtype=np.float, sep=' ')
                X[line_number - 1] = x
                
            line_number +=1

            if line_number % 10 == 0:
                print(line_number / n_rows)

    return X
        


if __name__ == "__main__":

        
    datapath = sys.argv[1]
    overfeat_binary = "../OverFeat/bin/macos/overfeat"
    overfeat_options = "-f"

    filename_to_row = {}

    class_to_filename = gather_files(datapath, exclude=None)
    n_rows, n_cols = get_matrix_row_n(class_to_filename), overfeat_feature_n()


    overfeat_input, y = create_overfeat_argument_list(class_to_filename)
    unique_file_id = hashlib.sha224("".join(overfeat_input).encode('utf-8')).hexdigest()

    X = run_overfeat(overfeat_input, n_rows, n_cols)

    # At this point we have the feature vectors in X, the class labels in y, and the filename to row mapping in overfeat_input
    np.savez(unique_file_id, X, y, input_file_mapping)

            


