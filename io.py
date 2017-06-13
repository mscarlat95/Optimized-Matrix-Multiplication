""" 
    Author: Cosmin-Gabriel Samoila
    Year: 2017
"""

import sys
import os
from utils import WrongParameterError, print_matrix
from utils import print_verbose

def parse_matrix(lines, no_rows, no_cols):
    result = []
    for line in lines:
        line = line.strip('\n\t ')
        if line == '':
            continue
        line = line.split(' ')
        if len(line) != no_cols:
            return None
        l = [float(i) for i in line]
        result.append(l)
    return result

def read_matrix_from_file(filename, no_rows, no_cols):
    try:
        print_verbose("Trying to read matrix from ", filename,
                      " with size ", no_rows, "x", no_cols) 
        f = open(filename)
        lines = f.readlines()
        return parse_matrix(lines, no_rows, no_cols)
    except:
        print "Failed to read matrix from " + filename
        return None

def write_matrix_to_file(filename, Mat):
    try:
        print_verbose("Trying to write matrix in ", filename)
        f = open(filename, 'w+')
        for line in Mat:
            three_decimal_row = ["%.3f" % i for i in line]
            line = ""
            for num in three_decimal_row:
                line += str(num) + " "
            f.write(line + "\n")
        f.close()
    except:
        print "Couldn't write matrix into file " + filename
        raise

# Use it only for test cases!!!
def read_file(filename="input.mat"):
    '''
       Method - 1 . All params in the same file.
       Legacy code!
       File format:
       TRANSA TRANSB ALPHA BETA LDA LDB LDC M N K
       A
       B
       C
    '''
    A = None
    B = None
    C = None
    lines = []
    params = {}
    try:
        f = open(filename, "r")
        lines = f.readlines()
    except:
        print "Failed to open/read from file: " + filename
        raise
    line = lines[0].split(' ')
    try:
        params['TRANSA'] = line[0]
        params['TRANSB'] = line[1]
        params['ALPHA'] = float(line[2])
        params['BETA'] = float(line[3])
        params['LDA'] = int(line[4])
        params['LDB'] = int(line[5])
        params['LDC'] = int(line[6])
        params['M'] = int(line[7])
        params['N'] = int(line[8])
        params['K'] = int(line[9])
        if params['LDA'] < 0 or\
           params['LDB'] < 0 or\
           params['LDC'] < 0 or\
           params['M'] < 0 or\
           params['N'] < 0 or\
           params['K'] < 0:
            raise WrongParameterError("One of the matrix dimensions is negative")
        # read matrix A[M][K]
        A = parse_matrix(lines[1:params['M'] + 1], params['M'], params['K'])
        # read matrix B[K][N]
        B = parse_matrix(lines[(params['M'] + 1):(params['M'] + params['K'] + 1)],
            params['K'], params['N'])
        # read matrix C
        C = parse_matrix(lines[(params['M']+params['K'] + 1):], params['M'], params['N'])
        print_matrix(A, "----Matrix A----", "----End of Matrix A----")
        print_matrix(B, "----Matrix B----", "----End of Matrix B----")
        print_matrix(C, "----Matrix C----", "----End of Matrix C----")
    except ValueError:
        print "Error when converting one of the parameters"
        raise
    except Exception as ex:
        raise
    if A == None or\
       B == None or\
       C == None:
        return None

    params['A'] = A
    params['B'] = B
    params['C'] = C
    f.close()
    return params
