#ifndef BAM_WRITER_H
#define BAM_WRITER_H

#include <string>
#include <sys/types.h>
#include <sys/stat.h>

#include "SamFile.h"
#include "Parameters.h"

using namespace std;

class BamWriter{


public:
	SamFile samFile;
	SamFileHeader samHeader;
	BamWriter(string bamFilePath, SamFileHeader samHeader_);

	bool writeRecord(SamRecord &samRecord);
	void close();
};
#endif