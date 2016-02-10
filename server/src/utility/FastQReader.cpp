#include "FastQReader.h"
using namespace std;

FastQReader::FastQReader(string FastQFilePath){
	fastQFile.openFile(FastQFilePath.c_str());
}


bool FastQReader::getNextSequence(FastQSequence &fastQSequence){
	if(fastQFile.keepReadingFile()){
    	fastQFile.readFastQSequence();
		fastQSequence.sequenceIdentifier =string(fastQFile.mySequenceIdentifier);
		fastQSequence.rawSequence = string(fastQFile.myRawSequence);
		fastQSequence.sequenceIdLine = string(fastQFile.mySequenceIdLine);
		fastQSequence.qualityString = string(fastQFile.myQualityString);
		fastQSequence.plusLine = string(fastQFile.myPlusLine);\
		return true;
    } else {
    	closeFile();
    	return false;
    }

}

bool FastQReader::closeFile(){
   fastQFile.closeFile();
   return 0;
}