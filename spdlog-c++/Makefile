main:main.o
	g++ main.o  -o main
main.o:
	g++ -c main.c -o main.o -I ./spdlog/include -std=c++11
clean:
	rm -rf *.o main
