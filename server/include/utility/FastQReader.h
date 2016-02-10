#ifndef FASTQ_READER_H
#define FASTQ_READER_H


#include <string>

#include "FastQFile.h"
#include "FastQSequence.h"
#include "FastQStatus.h"
using namespace std;

class FastQReader{


public:
	FastQFile fastQFile;
	FastQReader(string fastQFilePath);
	bool getNextSequence(FastQSequence &fastQSequence);
	bool closeFile();
};
#endif