#include "FastQWriter.h"
#include <cstdio>

FastQWriter::FastQWriter(string fastQFilePath){
	size_t next=0;
	while ((next=fastQFilePath.find("/",next+1,1))!=std::string::npos)
		mkdir(fastQFilePath.substr(0, next).c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
	fastQFile = fopen(fastQFilePath.c_str(), "w");
}

bool FastQWriter::writeSequence(FastQSequence &fastQSequence){
	fprintf(fastQFile, "%s\n",fastQSequence.sequenceIdLine.c_str());
	fprintf(fastQFile, "%s\n",fastQSequence.rawSequence.c_str());
	fprintf(fastQFile, "%s\n",fastQSequence.plusLine.c_str());
	fprintf(fastQFile, "%s\n",fastQSequence.qualityString.c_str());
}

