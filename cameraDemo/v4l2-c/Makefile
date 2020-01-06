objects = main.c play_video.c

exe : $(objects)

	#g++ -g -o exe $(objects) -L/usr/lib/x86_64-linux-gnu -I/usr/include -lv4l2 -lv4l1
	gcc $(objects) -o exe

clean:
	rm exe
