#ifndef FASTQ_WRITER_H
#define FASTQ_WRITER_H


#include <string>
#include <sys/types.h>
#include <sys/stat.h>
#include <cstdio>

#include "FastQFile.h"
#include "FastQSequence.h"

using namespace std;

class FastQWriter{


public:
	FILE* fastQFile;
	FastQWriter(string fastQFilePath);
	bool writeSequence(FastQSequence &fastQSequence);
	bool closeFile();
};
#endif