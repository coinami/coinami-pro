#include <iostream>
#include "Mux.h"
using namespace std;


int main( int argc,char *argv[]){
	Mux mux(argc-2, argv[1], argv+2);
	mux.mixFiles();
}
