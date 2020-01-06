# main:main.o
# 	g++ main.o -o main
# main.o:
# 	g++ -c main.cpp -o main.o

objects = main.cpp
exe : $(objects)
	g++ -o exe $(objects) -std=c++11 -I/usr/local/include -L/usr/local/lib -luvc \
	-I/usr/local/include/opencv -I/usr/local/include -L/usr/local/lib \
	-lopencv_dnn -lopencv_ml -lopencv_objdetect -lopencv_shape -lopencv_stitching -lopencv_superres -lopencv_videostab -lopencv_calib3d -lopencv_features2d -lopencv_highgui -lopencv_videoio -lopencv_imgcodecs -lopencv_video -lopencv_photo -lopencv_imgproc -lopencv_flann -lopencv_core
#-I/usr/local/include/opencv -I/usr/local/include -L/usr/local/lib 
#-I/opt/opencv3.4/include/opencv -I/opt/opencv3.4/include -L/opt/opencv3.4/lib

clean:
	rm -rf *.o exe
