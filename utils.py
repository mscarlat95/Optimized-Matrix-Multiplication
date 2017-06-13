"""" 
    Author: Cosmin-Gabriel Samoila
    Year: 2017
"""
import os
try:
     VERBOSE = bool(os.environ['VERBOSE'])
except:
     VERBOSE = False


def perror(message):
    print "ERROR: " + message
    sys.exit(1)

def print_verbose(*args):
    global VERBOSE
    if VERBOSE == False:
        return
    for arg in args:
        print arg,
    print

def f_equal(a, b, EPS = 0.001):
    if isinstance(a, float) and isinstance(b, float):
        if abs(a - b) <= EPS:
            return True
    return False



class WrongParameterError(Exception):
    """
    Raise this error when a parameter is worng:
    Eg: matrix dim < 0
    """
    def __init(self, message="", errors={}):
        super(WrongParameterError, self).__init__(message)
        self.errors = errors

def print_matrix(Mat, Top="", Bottom=""):
    if Top != "":
        print_verbose(Top)
    for line in Mat:
        three_decimal_row = ["%.3f" % i for i in line]
        line = ""
        for num in three_decimal_row:
            line += str(num) + " "
        print_verbose(line)
    if Bottom != "":
        print_verbose(Bottom)

def get_tests_config(filename="tema2.cfg"):
    """
       read config file line by line
       store each file as a dict {filename, N, M, num_range, valid}
       valid - True/False : True only if all 4 previous fields are ok
       return: a list of dicts(each dict is a matrix config)
    """
    print_verbose("Reading tests configuration from file ", filename)
    result = {}
    fname = filename
    try:
        fname = os.environ['CFG']
    except:
        fname = filename
    f = open(fname)
    lines = f.readlines()
    for line in lines:
        line = line.strip(' \n')
        if line == '' or\
           line.startswith('#') or\
           line.startswith('//') or\
           line.startswith('\\\\'):
            continue
        try:
            tokens = line.split('.')
            test_name = tokens[0].strip(' \n')
	    tokens = tokens[1].split('=')
            tokens = [token.strip(' \n') for token in tokens]
            key = tokens[0]
            value = tokens[1]
            if test_name not in result:
                result[test_name] = {}
            result[test_name][key] = value
            #print test_name + ":" + key + ":" + value
        except:
            result[test_name]['active'] = False
            print "Not a valid line. Test " + test_name + "is inactive"
    for test in result:
        try:
            result[test]['M'] = int(result[test]['M']) 
            result[test]['N'] = int(result[test]['N']) 
            result[test]['K'] = int(result[test]['K']) 
            result[test]['LDA'] = int(result[test]['LDA']) 
            result[test]['LDB'] = int(result[test]['LDB']) 
            result[test]['LDC'] = int(result[test]['LDC'])
            result[test]['ALPHA'] = float(result[test]['ALPHA'].replace(',','.')) 
            result[test]['BETA'] = float(result[test]['BETA'].replace(',','.'))
            result[test]['num_range'] = int(result[test]['num_range'])
            result[test]['points'] = int(result[test]['points'])
            result[test]['active'] = bool(result[test]['active'])
        except:
            result[test]['active'] = False
            print "One of " + test + "'s test parameters " +\
                  "cannot be converted from str to float/int/boolean"
    print_verbose(result)
    return result
