#ifndef MUX_H
#define MUX_H
#define MAX_NUM_FILES 100
#define THE_ANSWER_TO_EVERYTHING 42

#include "BamReader.h"
#include "FastQReader.h"
#include "FastQWriter.h"
#include "FastQSequence.h"
#include "DBHandler.h"
#include "SamFlag.h"
#include "CryptoHandler.h"

#include <string>
#include <cstring>
#include <map>
#include <set>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <unistd.h>

using namespace std;

class Mux{

	const int JOB_READ_COUNT = 100;
	const int NUM_DECOYS = 3;

	const string CONNECTION_STRING = string("postgresql://amicoin:amicoin1@localhost/amicoin");
	const string DECOY_FILE_PATH = "samples/decoy"; //should be without an extension
	const string OUTPUT_FOLDER_PATH = "muxout/";


	vector<FastQReader*> readers[2];
	map<string, SamRecord*> decoyResults[2];
	vector<FastQSequence*> decoyReads[2];

	FastQReader decoyFqReader[2];
	BamReader decoyBamReader;
	CryptoHandler cHandler;
	int numFiles;
	DBHandler db;
	int groupID;
	bool isClosed[MAX_NUM_FILES] = {false};
	int currentReadIndex[MAX_NUM_FILES] = {0};
	int fileID[MAX_NUM_FILES];

	string generateJobFileName(int groupID, int jobID);
	string generateDecoyLabel(string label,int jobID);
	string generateReadLabel(int fileIndex);
	void readDecoyFiles();
	int getRandomOpenFileIndex();
	void fillFilesWithDecoys(FastQWriter writer[2], int numDecoys,int jobID);
	void writeDecoy(FastQWriter &writer,int jobID, int decoyIndex, int pairIndex);

public:
	Mux(int numFiles_, string keyFile, char* filePaths[]);
	bool mixFiles();
};

#endif

