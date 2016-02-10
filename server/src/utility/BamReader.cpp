#include "BamReader.h"
using namespace std;

BamReader::BamReader(string bamFilePath){
    samFile.OpenForRead(bamFilePath.c_str());
    samFile.ReadBamIndex();    
    samFile.ReadHeader(samHeader);
}


bool BamReader::getNextRecord(SamRecord &samRecord){
    return samFile.ReadRecord(samHeader, samRecord);
}
SamFileHeader BamReader::getHeader(){
	return samHeader;
}


