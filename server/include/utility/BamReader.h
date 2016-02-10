#ifndef BAM_READER_H
#define BAM_READER_H

#include <string>

#include "SamFile.h"
#include "Parameters.h"

using namespace std;

class BamReader{


public:
	SamFile samFile;
	SamFileHeader samHeader;
	BamReader(string bamFilePath);

	bool getNextRecord(SamRecord &samRecord);
	SamFileHeader getHeader();
};
#endif
