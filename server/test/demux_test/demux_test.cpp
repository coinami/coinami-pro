#include <iostream>
#include "Demux.h"
using namespace std;


int main( int argc,char *argv[]){
	Demux demux(atoi(argv[1]),string(argv[2]),argv[3]);
	if(demux.verify()){
		demux.match();
		demux.authenticate();
	}
	else{
		demux.reject();
	}
	return 0;
}
