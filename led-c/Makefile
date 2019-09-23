main:main.o led.o
	gcc main.o led.o -o main
main.o:
	gcc -c main.c -o main.o
cpuinfo.o:
	gcc -c led.c -o led.o
clean:
	rm -rf *.o main
