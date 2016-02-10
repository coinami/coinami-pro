#ifndef FASTQ_SEQUENCE_H
#define FASTQ_SEQUENCE_H
#include <string>
#include <iostream>
using namespace std;
class FastQSequence{
public:
	string 	rawSequence;
	string 	sequenceIdLine;
	string 	sequenceIdentifier;
	string 	plusLine;
	string 	qualityString;
	void print();
};

#endif