#!/usr/bin/env python
""" 
    Author: Cosmin-Gabriel Samoila
    Year: 2017
"""
import multiprocessing
import sys
import os
import argparse
import datetime
from utils import f_equal
from utils import get_tests_config
from utils import print_verbose
from io import read_matrix_from_file

EXE_NAME='tema2'
tests = {}
def get_total_points(test_dict):
    total = 0
    return total

def check_results(ref_filename, out_filename, nrows, ncols):
    ref_matrix = read_matrix_from_file(ref_filename, nrows, ncols)
    out_matrix = read_matrix_from_file(out_filename, nrows, ncols)
    if ref_matrix == None:
        return (-1, "Reading REF matrix failed. Make sure the input " +\
                    "files are present and run <make>")
    if out_matrix == None:
        return (-2, "Reading OUT matrix failed. File " + out_filename +\
                    " doesn't exist or number of rows/cols is different from " +\
                    str(nrows) + "x" + str(ncols))
    for i in xrange(nrows):
        ref_line = ref_matrix[i]
        out_line = out_matrix[i]
        # checking the number of floats per line is performed in
        # read_matrix_from_file. If matrix isn't nrows x ncols, None is returned
        for j in xrange(ncols):
            if f_equal(ref_line[j], out_line[j], 0.005) == False:
                msg = "Different values in matrix at [{:d}][{:d}]".format(i ,j)
                return (1, msg)
    return (0, "OK")

def run_python():
    os.system("python main.py")

def run_native(timeout = 180, bonust = 45):
    
    p = multiprocessing.Process(target = run_code,
                                name = "Tema2_native")
    ret = None

    p.start()
    # Wait timeout for thread to end it's work
    p.join(bonust)
    if p.is_alive() == False:
	return (20,"OK")
    p.join(timeout - bonust)
    
    if p.is_alive():
        p.terminate()
        p.join()
        return (-1, "Timeout")
    return (0, "OK")

def run_code():
    global EXE_NAME
    os.system("./" + EXE_NAME)

def run_tests(timeout = 180,
              bonus_timeout = 45, 
              gen_python = False,
              gen_native = False):
    global tests
    total = 0
    partial = 0
    if gen_python == True:
        print "Runing python implementation"
        ts = datetime.datetime.now()
        run_python()
        te = datetime.datetime.now()
        print "Python implementation done in " + str(te - ts)

    if gen_native == True:
        print "Runing native implementation for maximum " +\
              str(timeout) + " seconds"
        ts = datetime.datetime.now()
        err = run_native(timeout, bonus_timeout)
        if err[0] == -1:
            print "Timeout occured (" + str(timeout) + "s): 0p"
            return
        elif err[0] == 20:
            total = 20
            partial = 20
            print "Bonus :", 20
        te = datetime.datetime.now()
        print "Native implementation done in " + str(te - ts)
    #run_native()
    for test in tests:
        M = tests[test]['M']
        N = tests[test]['N']
        total += tests[test]['points']
        ref_file = os.path.join("ref", test + ".ref")
        out_file = os.path.join("out", test + ".out")
        (err_code, err_msg) = check_results(ref_file, out_file, M, N)
        if err_code == 0:
            print "Test " + test + " ok:" + str(tests[test]['points']) + "p"
            partial += tests[test]['points']
        else:
            print "Test " + test + " failed 0/" + str(tests[test]['points'])\
                  + "p:" + err_msg
    print "Total points: " + str(partial) + "/" + str(total)

def main():
    global tests
    parser = argparse.ArgumentParser(description='Tema 2 tester')
    parser.add_argument('-t', metavar='TIMEOUT', type=int, nargs='?',
                              help='set timeout value in seconds')
    parser.add_argument('-bt', metavar='BTIMEOUT', type=int, nargs='?',
                              help='set bonus timeout value in seconds')
    parser.add_argument('-a', action='store_true', help='generate, run_python, run_native')
    parser.add_argument('-n', action='store_true', help='run native')
    parser.add_argument('-p', action='store_true', help='run python')
    args = parser.parse_args()
    timeout = 180
    bonus_timeout = 45 
    native = False
    python = False
    if args.a:
        print "Starting to generate input"
        os.system("make gen")
        native = True
        python = True
    else:
        native = args.n
        python = args.p
    if args.t != None:
        timeout = args.t
    if args.bt != None:
        bonus_timeout = args.bt
    
    tests = get_tests_config()
    run_tests(timeout, bonus_timeout, python, native)

if __name__ == '__main__':
    main()
