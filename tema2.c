#include "utils.h"
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 32
#define MAX 4001

void my_error(int flag, char *errtype, char *message)
{
    if (flag)
    {
        fprintf(stderr, "ERROR %s: %s\n", errtype, message);
        exit (-1);
    }
}

void read_matrix(FILE *fin, double *a, int N, int M, int transpose, double scalar)
{
    int fsize = -1, res = -1, i, j;
    char *buff, *current;

    if (transpose)
    {
        int temp = N;
        N = M;
        M = temp;
    }

    if (scalar == 0)
    {
        for (i = 0; i < N; ++i)
            for (j = 0; j < M; ++j)
                a[i * M + j] = 0;
    }

    /* Get file size */
    res = fseek (fin, 0, SEEK_END);
    my_error (res != 0, "Fseek", "Invalid pointer");
    fsize = ftell (fin);
    my_error (fsize < 0, "File size", "invalid");
    fseek (fin, 0, SEEK_SET);

    /* Obtain data */
    buff =  malloc (fsize * sizeof(char));
    res = fread (buff, fsize, 1, fin);

    current = strtok (buff, " ");

    if (scalar != 1)
    {
        for (i = 0; i < N; ++i)
            for (j = 0; j < M; ++j) {
                my_error (current == NULL, "strtok", "null pointer");
                a[i * M + j] = atof (current) * scalar;
                current = strtok (NULL, " ");
            }
    }
    else
    {
        for (i = 0; i < N; ++i)
            for (j = 0; j < M; ++j) {
                my_error (current == NULL, "strtok", "null pointer");
                a[i * M + j] = atof (current);
                current = strtok (NULL, " ");
            }
  
    }  
    free (buff);
}

int main(int argc, char **argv)
{
    struct test **tests;
    tests = (struct test **)malloc(sizeof(struct test*));
    (*tests) = (struct test *)calloc(MAXTESTS, sizeof(struct test));
    
    if (argc != 2)
        error("Usage: tema2 <cfg_file>");
    
    parse_config(argv[1], tests);
    // print_tests(*tests);

    FILE *fin, *fout;
    int i, j, p, k = 0;
    int sz1, sz2, sz3, ii, jj, pp;
    char fnameA[50], fnameB[50], fnameC[50], output[50];
    struct test *current_test = &((*tests)[k]);
    register double temp = 0;

    int M, N, K;
    double *A, *B, *C;
    double alpha, beta;
    int tA = -1, tB = -1;

    /* Memory allocation */
    A = malloc (MAX * MAX * sizeof(double));
    B = malloc (MAX * MAX * sizeof(double));
    C = malloc (MAX * MAX * sizeof(double));

    while (current_test != NULL && current_test->name[0] != '\0')
    {
        /* Set file names */
        memset (&fnameA, 0, 50 * sizeof(char));
        sprintf(fnameA, "./input/%s_A.in", current_test->name);
        memset (&fnameB, 0, 50 * sizeof(char));
        sprintf(fnameB, "./input/%s_B.in", current_test->name);
        memset (&fnameC, 0, 50 * sizeof(char));
        sprintf(fnameC, "./input/%s_C.in", current_test->name);

        /* Set N, M, K */
        N = current_test->N;
        M = current_test->M;
        K = current_test->K;

        /* Set transpose, alpha and beta*/
        tA = current_test->transa == 'T';
        tB = current_test->transb == 'T';
        alpha = current_test->alpha;
        beta = current_test->beta;

        /* Read matrix A */
        fin = fopen(fnameA, "r");
        my_error(fin == NULL, "Opening file ", fnameA);
        read_matrix (fin, A, M, K, tA, alpha);
       	fclose (fin);
 
        /* Read matrix B */
        fin = fopen(fnameB, "r");
        my_error(fin == NULL, "Opening file ", fnameB);
        read_matrix (fin, B, K, N, tB, 1);
        fclose (fin);


        /* Read matrix C */
        fin = fopen(fnameC, "r");
        my_error(fin == NULL, "Opening file ", fnameC);
        read_matrix (fin, C, M, N, 0, beta);
        fclose(fin);

        /* case N N */
        if (!tA && !tB)
        {
    		for (ii = 0; ii < N/BLOCK_SIZE + 1; ++ii)
    		{
    			for (jj = 0; jj < K/BLOCK_SIZE + 1; ++jj)
    			{
    				for (pp = 0; pp < M/BLOCK_SIZE + 1; ++pp)
    				{
    					sz1 = (ii+1) * BLOCK_SIZE;
    					if (sz1 > N)
    						sz1 = N;
    					for (i = ii * BLOCK_SIZE; i < sz1; ++i)
			    		{
			    			sz2 = (jj+1) * BLOCK_SIZE;
	    					if (sz2 > K)
	    						sz2 = K;
			    			for (j = jj * BLOCK_SIZE; j < sz2; ++j)
			    			{
			    				sz3 = (pp+1) * BLOCK_SIZE;
		    					if (sz3 > M)
		    						sz3 = M;
			    				temp = B[j*N + i];
			    				for (p = pp * BLOCK_SIZE; p < sz3; ++p)
			    				{
			    					C[p * N + i] +=  temp * A[p*K + j];
			    				}
			    			}
			    		}
			    	}
    			}
    		}
        }
        else if (!tA && tB) /* case N T */
        {
            for (ii = 0; ii < N/BLOCK_SIZE + 1; ++ii)
            {
                for (jj = 0; jj < K/BLOCK_SIZE + 1; ++jj)
                {
                    for (pp = 0; pp < M/BLOCK_SIZE + 1; ++pp)
                    {
                        sz1 = (ii+1) * BLOCK_SIZE;
                        if (sz1 > N)
                            sz1 = N;
                        for (i = ii * BLOCK_SIZE; i < sz1; ++i)
                        {
                            sz2 = (jj+1) * BLOCK_SIZE;
                            if (sz2 > K)
                                sz2 = K;
                            for (j = jj * BLOCK_SIZE; j < sz2; ++j)
                            {
                                sz3 = (pp+1) * BLOCK_SIZE;
                                if (sz3 > M)
                                    sz3 = M;

                                temp = B[i*K + j];
                                for (p = pp * BLOCK_SIZE; p < sz3; ++p)
                                {
                                    C[p * N + i] +=  temp * A[p*K + j];
                                }
                            }
                        }
                    }
                }
            }
        }
        else if (tA && !tB) /* case T N */
        {
        	for (ii = 0; ii < N/BLOCK_SIZE + 1; ++ii)
    		{
    			for (jj = 0; jj < M/BLOCK_SIZE + 1; ++jj)
    			{
    				for (pp = 0; pp < K/BLOCK_SIZE + 1; ++pp)
    				{
    					sz1 = (ii+1) * BLOCK_SIZE;
    					if (sz1 > N)
    						sz1 = N;
    					for (i = ii * BLOCK_SIZE; i < sz1; ++i)
			    		{
			    			sz2 = (jj+1) * BLOCK_SIZE;
	    					if (sz2 > M)
	    						sz2 = M;
			    			for (j = jj * BLOCK_SIZE; j < sz2; ++j)
			    			{
			    				sz3 = (pp+1) * BLOCK_SIZE;
		    					if (sz3 > K)
		    						sz3 = K;

			    				temp = 0;
			    				for (p = pp * BLOCK_SIZE; p < sz3; ++p)
			    				{
			    					temp += A[p * M + j] * B[p * N + i];
			    				}
			    				C[j * N + i] += temp;
			    			}
			    		}
			    	}
    			}
    		}
        }
        else if (tA && tB) /* case T T */
        {
        	for (ii = 0; ii < N/BLOCK_SIZE + 1; ++ii)
    		{
    			for (jj = 0; jj < M/BLOCK_SIZE + 1; ++jj)
    			{
    				for (pp = 0; pp < K/BLOCK_SIZE + 1; ++pp)
    				{
    					sz1 = (ii+1) * BLOCK_SIZE;
    					if (sz1 > N)
    						sz1 = N;
    					for (i = ii * BLOCK_SIZE; i < sz1; ++i)
			    		{
			    			sz2 = (jj+1) * BLOCK_SIZE;
	    					if (sz2 > M)
	    						sz2 = M;
			    			for (j = jj * BLOCK_SIZE; j < sz2; ++j)
			    			{
			    				sz3 = (pp+1) * BLOCK_SIZE;
		    					if (sz3 > K)
		    						sz3 = K;

			    				temp = 0;
			    				for (p = pp * BLOCK_SIZE; p < sz3; ++p)
			    				{
			    					temp += A[p * M + j] * B[i * K + p];
			    				}
			    				C[j * N + i] += temp;
			    			}
			    		}
			    	}
    			}
    		}
        }

        memset(&output, 0, sizeof(output));
        sprintf(output, "./out/%s.out", current_test->name);
        fout = fopen(output, "w");
        for (i = 0; i < M; ++i)
        {
            for (j = 0; j < N; ++j)
                fprintf(fout, "%.3lf ", C[i * N + j]);
            fprintf(fout, "\n");
        }
        fclose (fout);

        /* Next test */
        ++ k;
        current_test = &((*tests)[k]);
    }

    /* Release memory */
    free (A);
    free (B);
    free (C);
    
    return 0;
}
