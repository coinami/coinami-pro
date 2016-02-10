#include<iostream>
#include "BamReader.h"
using namespace std;

int main(){
	string inFile = "samples/decoy1.bam";
	BamReader bamReader(inFile);
	SamRecord result;
	while(bamReader.getNextRecord(result)){
		cout  << result.getReadName() << endl;
	}
}
