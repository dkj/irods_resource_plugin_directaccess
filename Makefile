GCC =g++ 
INC	=-I/usr/include/irods/ -I./include/ 
CFLAGS =-g -Wall

all:
	${GCC} ${INC} $(CFLAGS) -Dlinux_platform -fPIC -shared -o libdirectaccess.so ./src/libdirectaccess.cpp /usr/lib/libirods.a
	
clean:
	@-rm -f *.so > /dev/null 2>&1
