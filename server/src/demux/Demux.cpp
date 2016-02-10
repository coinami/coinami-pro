#include "Demux.h"
#include <unistd.h>

using namespace std;

Demux::Demux(int jobID_,string keyFile, string outputFolder_):
	cHandler(keyFile){
	jobID = jobID_;
	db.connect(CONNECTION_STRING);
	bamFilePath = db.getResultFile(jobID);
	cout << bamFilePath << endl; 	
	outputFolder = outputFolder_;
}


bool Demux::isDecoy(string recordName){
	//starts with DECOY.
	return recordName.find("DECOY") == 0;
}

string Demux::generateFileName(string recordName){
	string temp = outputFolder+'/';
	return temp.append(recordName.substr(0,recordName.find_last_of("."))+string("/job")+to_string(jobID));
}

bool Demux::verify(){ //at least one decoy should be present
	BamReader bamReader(bamFilePath);
	SamRecord samRecord;
	int verifiedDecoys = 0;
	while (	bamReader.getNextRecord(samRecord)) {
		string recordName(samRecord.getReadName());
		recordName = cHandler.decrypt(recordName);
		//clean record name
		int len=recordName.find("$");
		recordName=recordName.substr(0,len);
		//clean ended
		if (isDecoy(recordName)){
			char decoyChromosome[2][20];
			int decoyLocation[2];
			int decoyJobID;

			sscanf(	recordName.c_str(),"DECOY.%[^.].%d_%[^.].%d.%d",
					decoyChromosome[0], decoyLocation, 
					decoyChromosome[1], decoyLocation + 1,  &decoyJobID);

			int pair = 	!SamFlag::isFirstFragment(samRecord.getFlag());
			if (strcmp(decoyChromosome[pair],samRecord.getReferenceName())){
				cout << "Chromosome mismatch\n";
				cout << "Expected: " << decoyChromosome[pair] << endl;
				cout << "Got: " << samRecord.getReferenceName() << endl;
				return false;
			}
			if ( decoyLocation[pair] != samRecord.get0BasedPosition()){
				cout << "Position mismatch\n";
				cout << "Expected: " << decoyLocation[pair] << endl;
				cout << "Got: " << samRecord.get0BasedPosition() << endl;
				return false;
			}
			if (decoyJobID != jobID){
				cout << "Job ID mismatch\n";
				cout << "Expected: " << decoyJobID << endl;
				cout << "Got: " << jobID << endl;
				return false;
			}
			verifiedDecoys++;
		}
    }
    if (verifiedDecoys)
		return true;
	else
		return false;
}

void Demux::match(){
	BamReader bamReader(bamFilePath);
	SamRecord samRecord;
	while (	bamReader.getNextRecord(samRecord)) {
		string recordName(samRecord.getReadName());
		recordName = cHandler.decrypt(recordName);
		//clean record name
		int len=recordName.find("$");
		recordName=recordName.substr(0,len);
		//clean ended
		if (!isDecoy(recordName)){
			string outputFile = generateFileName(recordName);
			printf("%s\n",outputFile.c_str());
			if (writers.find(outputFile) == writers.end()) //if the BamWriter is not initialized
				writers[outputFile] = new BamWriter(outputFile, bamReader.getHeader());
			BamWriter *writer = writers[outputFile];
			writer->writeRecord(samRecord);
		}
    }
    for(auto it=writers.begin();it!=writers.end();it++){
    	BamWriter *writer = it->second;
    	writer->close();
    	delete writer;
    }
}

void Demux::authenticate(){
	cout << "verified the job\n"; 
	db.completeJob(jobID);
}

void Demux::reject(){
	cout << "rejected the job\n";
	db.unassignJob(jobID);
}
