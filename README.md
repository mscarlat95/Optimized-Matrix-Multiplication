# README #

Implement in C/C++ a solver that has the same functionality as
solver.py: Matrix Matrix multiply from BLAS DGEMM
http://www.netlib.org/lapack/explore-html/d7/d2b/dgemm_8f_source.html

Tests:
    Part 1 Testing the implementation(70 p):
        IMPORTANT: if your implementation solves all the 8 tests in more
        than 180 seconds, you will lose all the 70 points.
        1. functionality_NN/TN/NT/TT: 4 tests with M = N = K = 1000
            Ok run time: 1 s each test
            Good run time: 0.2 s each test
            Points: 5p each test

        2. test1: M = 2000, N = 2000, K = 1000
            Ok run time: 3 s
            Good run time: 1.2 s
            Points: 10 p

        3. test2: M = 2000, N = 4000, K = 4000
            Ok run time: 6 s
            Good run time: 2 s
            Points: 10 p

        4. test3: M = 2000, N = 4000, K = 4000
            Ok run time: 10 s
            Good run time: 3.1 s
            Points: 10 p

        5. test1: M = 4000, N = 4000, K = 4000
            Ok run time: 15 s
            Good run time: 5 s
            Points: 20 p

    Part 2 Explain the results(30 p):
        IMPORTANT: you lose all 30 points if all any of the functionality tests
        is failing.
        1. Explain the results you obtained using different architectures
        and input sizes
        2. Build charts that are relevant for your implementation and results
        obtained at 1.

    Part 3 Bonus(20 p):
        IMPORTANT: you will get bonus points only if you have Part 1 and Part 2
        1. Your implementation must solve all the tests in less than 45 seconds.

Other information that might be useful to you:
Input: 'input' folder:
    1. tema2.cfg - default configuration file for tests.
    2. input/_test_name'_A.in'/'_B.in'/'_C.in' - all 3 input matrices
          for _test_name
          Eg: for a test with A[N][M], inputA contains
              N lines, each line having M floats. Same
              for B and C.

Output: 'out' folder. Each _test_ results must be written in
        out/_test_name.out.
         Eg: for a testname with matrices sizes M x K x N
             out/testname.out contains M lines with N floats per line

    ./input_generator.py - reads test2.cfg or CFG environment variable and
        generates input files(A,B and C matrices)
    ./tester.py - starts the tester
            Options: -a : generates input, runs python dgemm(obtains out files)
                        and runs native dgemm(obtains ref files). Atm native
                        exec is a copy of python solver and you will have to
                        implement your own exec in C/C++
                     -t TIMEOUT : runs the native code for max TIMEOUT seconds
                        If your implementation exceeds TIMEOUT, you will lose
                        all your points
                     -p : runs only python solver(make sure you have input files)
                          and compares out/* with ref/*
                     -n : runs only native solver(make sure you have input files)
                          and compares out/* with ref/*
                     -h : help message

    solver.py - contains dgemm implementation translated from Python
