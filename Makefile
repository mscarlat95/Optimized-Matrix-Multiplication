build: tema2.c utils.c utils.h
	gcc -O1 -ftree-vectorize -funroll-loops -fexcess-precision=fast -Wall -g -o tema2 utils.c tema2.c
run: build
	./tema2 tema2.cfg
verbose: tema2.c utils.c utils.h
	gcc -D VERBOSE -Wall -o tema2 utils.c tema2.c

clean:
	-rm -rf tema2 a.out
