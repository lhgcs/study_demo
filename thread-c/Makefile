CC=gcc #arm-linux-gnueabihf-gcc
CFLAGS=-Wall 

TARGET=main
SRCS = main.c memoryutil.c threadutil.c processutil.c
# INC = -I/usr/include


OBJS=$(SCR:.c=.o)

$(TARGET):$(SRCS)
	$(CC) $(FLAGS) -pthread -o $@ $^

clean:
	rm -rf $(TARGET) *.o *~