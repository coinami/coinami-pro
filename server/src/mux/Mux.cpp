#include "Mux.h"

/*
	Takes number of files: numFiles_; the real job files
	A key file: keyFile; the file that contains symmetric key for encryption
	File path strings: filePaths; the char* array that containts job file paths.
*/
Mux::Mux(int numFiles_, string keyFile, char* filePaths[]):
		decoyFqReader{
		FastQReader(DECOY_FILE_PATH + string(".1.fq")),
		FastQReader(DECOY_FILE_PATH + string(".2.fq"))},
		decoyBamReader(DECOY_FILE_PATH + string(".bam")),
		cHandler(keyFile){
	db.connect(CONNECTION_STRING);
	groupID = db.newGroupID();
	numFiles =  numFiles_;
	for(int i=0;i<numFiles;i++){
		isClosed[i]=false;
		string fileName = string(filePaths[i]);
		readers[0].push_back(new FastQReader(fileName+".1.fq"));
		readers[1].push_back(new FastQReader(fileName+".2.fq"));
		fileID[i] = db.newFastQFile(groupID, fileName, false);
	}
	srand((unsigned)time(NULL));
	readDecoyFiles();
}

void Mux::readDecoyFiles(){
	FastQSequence* sequence;
	SamRecord* result;
	while(decoyFqReader[0].getNextSequence(*(sequence = new FastQSequence()))){
		decoyReads[0].push_back(sequence);
		decoyFqReader[1].getNextSequence(*(sequence = new FastQSequence()));
		decoyReads[1].push_back(sequence);
	}
	while(decoyBamReader.getNextRecord(*(result = new SamRecord())))
		if(SamFlag::isFirstFragment(result->getFlag()))
			decoyResults[0][result->getReadName()] = result;
		else
			decoyResults[1][result->getReadName()] = result;
}

bool Mux::mixFiles(){
	// this will at each step select one file randomly.
	// and put the next sequence to the current partial fq output file.
	int closedFileCount = 0;
	int jobCount = 0;
	set<int> decoys;
	set<int>::iterator nextDecoy;
	
	while(closedFileCount < numFiles){
		jobCount++;
		decoys.clear();
		while(decoys.size() < NUM_DECOYS)
			decoys.insert(rand()%JOB_READ_COUNT);
		nextDecoy = decoys.begin();

		string fileName = generateJobFileName(groupID, jobCount);
		FastQWriter writer[2]={FastQWriter("job.1.fq"),FastQWriter("job.2.fq")};
		//
		int jobID = db.newJob(groupID, fileName+".zip");
		for(int i=0; i < JOB_READ_COUNT; i++){
			//randomly decide whether put from decoy or a real file
			if(nextDecoy != decoys.end() && *nextDecoy == i) { //if decoy
				int decoyIndex = rand() % decoyReads[0].size();
				writeDecoy(writer[0],jobID, decoyIndex, 0);
				writeDecoy(writer[1],jobID, decoyIndex, 1);
				++nextDecoy;
			}
			else { //if real file
				int fileIndex = getRandomOpenFileIndex();
				FastQSequence sequence[2];
				FastQReader* reader[2];
				reader[0] = readers[0][fileIndex];
				reader[1] = readers[1][fileIndex];
				if(reader[0] -> getNextSequence(sequence[0])){
					reader[1] -> getNextSequence(sequence[1]);
					string label = generateReadLabel(fileIndex);
					sequence[0].sequenceIdLine = label + "/1";
					sequence[1].sequenceIdLine = label + "/2";
					writer[0].writeSequence(sequence[0]);
					writer[1].writeSequence(sequence[1]);
				} else {
					isClosed[fileIndex] = true;
					if (++closedFileCount == numFiles) { // out of files to read
						fillFilesWithDecoys( writer, JOB_READ_COUNT - i + 1, jobID);
						break;
					}
				}
			} 
		}
		fclose(writer[0].fastQFile);
		fclose(writer[1].fastQFile);
		//this is a quick solution, needs to be fixed.
		size_t next=0;
		while ((next=fileName.find("/",next+1,1))!=std::string::npos)
			mkdir(fileName.substr(0, next).c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
		char command[512];
		sprintf(command,"zip %s.zip job.1.fq job.2.fq;rm job.1.fq job.2.fq;",fileName.c_str());
		system(command);
	}
	return true;
}

void Mux::writeDecoy(
	FastQWriter &writer, int jobID, int decoyIndex, int pairIndex){
 	FastQSequence* decoyRead = decoyReads[pairIndex][decoyIndex]; 
	string label = decoyRead->sequenceIdentifier;
	label = label.substr(0,label.find_last_of('/'));
	decoyRead->sequenceIdLine = generateDecoyLabel(label, jobID);
	writer.writeSequence(*decoyRead);
}

int Mux::getRandomOpenFileIndex(){
	int fileIndex;
	while( isClosed[fileIndex = (rand() % numFiles)]);
	return fileIndex;
}

void Mux::fillFilesWithDecoys(
		FastQWriter writer[2], int numDecoys, int jobID){
	for(int i=0; i<numDecoys; i++){
		int decoyIndex = rand() % decoyReads[0].size();
		writeDecoy(writer[0], jobID, decoyIndex, 0);
		writeDecoy(writer[1], jobID, decoyIndex, 1);
	}
}

string Mux::generateReadLabel(int fileIndex){
	// this will generate a label, according to which file is this read from
	char str[43];
	memset(str,0,43);
	sprintf(str, "FASTQ%d.READ%d", fileID[fileIndex], ++currentReadIndex[fileIndex]);


	int len=strlen(str);
	for(int i=len;i<THE_ANSWER_TO_EVERYTHING;++i)
		str[i]='$';
	str[THE_ANSWER_TO_EVERYTHING]='\0';
	string cipher = cHandler.encrypt(string(str));
	return "@"+cipher;
}

string Mux::generateDecoyLabel(string label,int jobID){
	// @DECOY.chr1.156433.336
	// chromosome:chr1 
	// location:156433 
	// jobID:336
	char str[THE_ANSWER_TO_EVERYTHING+1];
	memset(str,0,43);
	SamRecord *decoyResult[2]={decoyResults[0][label],decoyResults[1][label]};
	sprintf(str, "DECOY.%s.%d_%s.%d.%d",
			decoyResult[0]->getReferenceName(), decoyResult[0]->get0BasedPosition(),
			decoyResult[1]->getReferenceName(), decoyResult[1]->get0BasedPosition(), 
			jobID);
	int len=strlen(str);
	for(int i=len;i<THE_ANSWER_TO_EVERYTHING;++i)
		str[i]='$';
	str[THE_ANSWER_TO_EVERYTHING]='\0';
	string cipher = cHandler.encrypt(str);
	return "@"+cipher;
}

string Mux::generateJobFileName(int groupID, int jobID){
	char result[1024];
	sprintf(result,"%sgroup%d/job%d",OUTPUT_FOLDER_PATH.c_str(),groupID,jobID);
	return string(result);	
}
