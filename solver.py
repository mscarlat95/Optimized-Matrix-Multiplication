""" 
    Author: Cosmin-Gabriel Samoila
    Year: 2017
"""

import sys
from io import read_file
from utils import print_matrix, f_equal, perror
from utils import print_verbose
'''
    *  Double BLAS Level 3
    *  http://www.netlib.org/lapack/explore-html/d7/d2b/dgemm_8f_source.html
    *  Author:
    *  =======
    *  Cosmin-Gabriel Samoila
'''
def f_dgemm(TRANSA, TRANSB,
          M, N, K,
          ALPHA, A, LDA,
          B, LDB,
          BETA, C, LDC):
    """ Return Alpha * A * B + C.
    N N : A[M][K] * B[K][N] + C[M][N]
    N T : A[M][K] * B[N][K] + C[M][N] -> N = K
    T N : A[K][M] * B[K][N] + C[M][N] -> M = K
    T T : A[K][M] * B[N][K] + C[M][N] -> M = N = K  
    Keyword arguments:
    ========================================================
    M -- int M >= 0, number of rows of the matrix A and C
    N -- int N >= 0, number of columns of the matrix B and C
    K -- int K >= 0, number of columns of the matrix A and B
    ALPHA -- double precision float scalar aplha
    A -- matrix of double precision floats [LDA][ka]
        ka -- K for TRANSA // m otherwise
        LDA -- integer : first dimension of A. 
                When TRANSA = 'N', LDA = max(1, M),
                otherwise LDA = max(1, K)
    B -- matrix of double precision floats [LDB][kb]
        kb -- N for TRANSB // k otherwise
        LDB -- integer : first dimension of B.
                When TRANSB = 'N', LDB = max(1, K),
                otherwise LDB = max(1, N)
    BETA -- double precision float scalar beta
    C -- matrix of double precision floats [LDC][n].
        Matrix C will be overwritten with the result matrix
        LDC - first dimension of matrix C, equal to max(1, M).
    ==========================================================
    """
    nota = (TRANSA == 'N')
    notb = (TRANSB == 'N')
    #check if A is transposed
    nrowa = K
    ncola = M
    if nota:
        print_verbose("Matrix A is not transposed")
        nrowa = M
        ncola = K
    
    #check if B is transposed
    nrowb = N
    if notb:
        print_verbose("Matrix B is not transposed")
        nrowb = K
    
    '''
       Test input parameters
    '''
    if not nota and TRANSA != 'C' and TRANSA != 'T':
        perror("Wrong TRANSA parameter")
    elif not notb and TRANSB != 'C' and TRANSB != 'T':
        perror("Wrong TRANSB parameter")
    elif M < 0:
        perror("M < 0")
    elif N < 0:
        perror("N < 0")
    elif K < 0:
        perror("K < 0")
    elif LDA < max(1, nrowa):
        perror("LDA lower than max(1, A_#rows)") 
    elif LDB < max(1, nrowb):
        perror("LDB lower than max(1, B_#rows)")
    elif LDC < max(1, M):
        perror("LDC lower than max(1, m)")
    print_verbose("Alpha:", ALPHA)
    print_verbose("Beta:", BETA)
    # Quick return
    if M == 0\
       or N == 0\
       or ((f_equal(ALPHA, 0.0) or (K == 0)) and f_equal(BETA, 1.0)):
        return C
    
    # If ALPHA is 0.0
    if f_equal(ALPHA, 0.0):
        if f_equal(BETA, 0.0):
            for j in xrange(1, N):
                for i in xrange(1, M):
                    C[i][j] = 0.0
        else:
            for j in xrange(1, N):
                for i in xrange(1, M):
                    C[i][j] = BETA * C[i][j]

    # Start the operations
    if notb:
        if nota:
            # Form C := alpha*A*B + beta*C
            for j in xrange(N):
                if f_equal(BETA, 0.0):
                    for i in xrange(M):
                        C[i][j] = 0.0
                elif not f_equal(BETA, 1.0):
                    for i in xrange(M):
                        C[i][j] = BETA * C[i][j]
                for l in xrange(K):
                    temp = ALPHA * B[l][j]
                    for i in xrange(M):
                        C[i][j] = C[i][j] + temp * A[i][l]
        else:
            # FORM C := alpha*A**T*B + beta*C
            for j in xrange(N):
                for i in xrange(M):
                    temp = 0.0
                    for l in xrange(K):
                        temp = temp + A[l][i] * B[l][j]
                    if f_equal(BETA, 0.0):
                        C[i][j] = ALPHA * temp
                    else:
                        C[i][j] = ALPHA * temp + BETA * C[i][j]
    else:
        if nota:
            # Form C := alpha*A*B**T + beta*C
            for j in xrange(N):
                if f_equal(BETA, 0):
                    for i in xrange(M):
                        C[i][j] = 0.0
                elif not f_equal(BETA, 1.0):
                    for i in xrange(M):
                        C[i][j] = BETA * C[i][j]
                for l in xrange(K):
                    #print K, len(B[j])
                    temp = ALPHA * B[j][l]
                    for i in xrange(M):
                        C[i][j] = C[i][j] + temp * A[i][l]
        else:
            # Form C := alpha*A**T*B**T + beta*C
            for j in xrange(N):
                for i in xrange(M):
                    temp = 0.0
                    for l in xrange(K):
                        temp = temp + A[l][i]*B[j][l]
                    if f_equal(BETA, 0.0):
                        C[i][j] = ALPHA * temp
                    else:
                        C[i][j] = ALPHA * temp + BETA * C[i][j]
    # End of function
    return C
