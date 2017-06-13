#!/usr/bin/env python
import sys
import os
from random import randint
from utils import get_tests_config
from io import write_matrix_to_file
def generate_line(N = 128, num_range = 1024):
    row = []
    # multiply with 1000 and then divide a float
    # by 1000 to obtain a random float with 3 decimals
    rng = num_range * 1000
    for i in xrange(N):
        n = float(randint(0, rng))
        n /= 1000.0
        row.append(n)
    return row

def generate_matrix(N, M, num_range):
    mat = []
    for j in xrange(N):
        line = generate_line(M, num_range)
        mat.append(line)
    return mat

def generate_file(filename, N, M, num_range):
    f = open(filename, 'w+')
    matrix = generate_matrix(N, M, num_range)
    for line in matrix:
        line = [str(n) for n in line]
        line = ' '.join(line)
        f.write(line + '\n')
    f.close()

if __name__ == '__main__':
    tests = get_tests_config() 
    if os.path.exists("./input"):
        os.system("rm -rf ./input")
    os.system("mkdir ./input")
    os.chdir("./input")
    for test in tests:
        # test can be inactive because we chosen so
        # or an error happend while parsing the config
        if not tests[test]['active']:
            continue

        # generate A matrix and form filename: test_name_A.in
        fnameA = test.strip(" \n\t") + "_A.in"
        A = generate_matrix(tests[test]['M'],
                            tests[test]['K'],
                            tests[test]['num_range'])
        write_matrix_to_file(fnameA, A)

        # generate B matrix and form filename: test_name_B.in
        fnameB = test.strip(" \n\t") + "_B.in"
        B = generate_matrix(tests[test]['K'],
                            tests[test]['N'],
                            tests[test]['num_range'])
        write_matrix_to_file(fnameB, B)

        # generate C matrix and form filename: test_name_C.in
        fnameC = test.strip(" \n\t") + "_C.in"
        C = generate_matrix(tests[test]['M'],
                            tests[test]['N'],
                            tests[test]['num_range'])
        write_matrix_to_file(fnameC, C)
 
    """Example:
    params = {}
    params['filename'] = "my_input.txt"
    params['N'] = 4
    params['M'] = 5
    params['num_range'] = 32
    generate_file(**params)
    """
