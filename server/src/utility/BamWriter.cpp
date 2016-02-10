#include "BamWriter.h"
BamWriter::BamWriter(string bamFilePath, SamFileHeader samHeader_){
	samHeader = samHeader_;
	bamFilePath = bamFilePath +".bam";
	size_t next=0;
	while ((next=bamFilePath.find("/",next+1,1))!=std::string::npos)
		mkdir(bamFilePath.substr(0, next).c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
	samFile.OpenForWrite(bamFilePath.c_str());
   	samFile.WriteHeader(samHeader);
 }

bool BamWriter::writeRecord(SamRecord &samRecord){
	samFile.WriteRecord(samHeader, samRecord);
}

void BamWriter::close()
{
	samFile.Close();
}