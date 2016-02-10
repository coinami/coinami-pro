#include<iostream>
#include "FastQReader.h"
using namespace std;

int main(){
	string inFile = "samples/sample1.fq";
	FastQReader fastQReader(inFile);
	FastQSequence sequence;
	while(fastQReader.getNextSequence(sequence)){
		//sequence.print();
	}
	return 0;
}
