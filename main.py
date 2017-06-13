#!/usr/bin/env python

import os
import datetime
from solver import f_dgemm
from io import read_matrix_from_file
from io import write_matrix_to_file
from utils import get_tests_config, print_matrix
from utils import print_verbose
if __name__ == '__main__':
    tests = get_tests_config()
    if os.path.exists("./ref"):
        os.system("rm -rf ./ref")
    os.system("mkdir ref")
    for test in tests:
        fnameA = os.path.join("input", test.strip(" \n\t") + "_A.in")
        fnameB = os.path.join("input", test.strip(" \n\t") + "_B.in")
        fnameC = os.path.join("input", test.strip(" \n\t") + "_C.in")
        fnameRes = os.path.join("ref", test.strip(" \n\t") + ".ref")
        # skip test if one matrix file does not exists or test is inactive
        if not os.path.exists(fnameA) or\
           not os.path.exists(fnameA) or\
           not os.path.exists(fnameA) or\
           not tests[test]['active']:
            print "Ignoring test " + test
            print "Make sure input matrix files exist, tema2.cfg params "+\
                  "are ok and test is active."
            continue
        A = read_matrix_from_file(fnameA,
                                  tests[test]['M'],
                                  tests[test]['K'])


        B = read_matrix_from_file(fnameB,
                                  tests[test]['K'],
                                  tests[test]['N'])
        
        C = read_matrix_from_file(fnameC,
                                  tests[test]['M'],
                                  tests[test]['N'])
        params = tests[test]
        print_verbose("Runing test", test)
        ts = datetime.datetime.now()
        result = f_dgemm(params['TRANSA'], params['TRANSB'],
            params['M'], params['N'], params['K'],
            params['ALPHA'], A, params['LDA'],
            B, params['LDB'],
            params['BETA'], C, params['LDC'])
        te = datetime.datetime.now()
        print_verbose("Test ", test, "done in", te-ts)
        #print_matrix(A, "-----Matrix A-----", "----------")
        #print_matrix(B, "-----Matrix B-----", "----------")
        #print_matrix(C, "-----Matrix C-----", "----------")
        top = "----Test " + test + ": " + str(params['ALPHA']) +\
          "*A*B + " + str(params['BETA']) + "*C----"
        #print_matrix(result, top, "--------")
        write_matrix_to_file(fnameRes, result)



