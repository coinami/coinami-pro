#ifndef DEMUX_H
#define DEMUX_H
#define THE_ANSWER_TO_EVERYTHING 42

#include "BamReader.h"
#include "BamWriter.h"
#include "DBHandler.h"
#include "CryptoHandler.h"
#include "SamFlag.h"
#include <string>
#include <cstring>
#include <map>

using namespace std;

class Demux{
	map<string, BamWriter* > writers;
	bool isDecoy(string recordName);
	string generateFileName(string recordName);

	const string CONNECTION_STRING = string("postgresql://amicoin:amicoin1@95.85.3.36/coinami");
	int jobID;
	DBHandler db;
	string outputFolder = "demuxout";
	CryptoHandler cHandler;


public:
	string bamFilePath;
	Demux(int jobID_, string keyFile, string outputFolder_);

	// 	This function will go through each alignment info in the Bam file, detect
	// decoys by decrypting the labels using CryptoHandler and verify their alignment. If
	// everything’s OK, it will return true and mark the particular FastQ files as verified in
	// database.
	bool verify();

	// 	 This function will create different BamFiles, seperating them if they are originally
	// from different fastQ files.
	void match();

	// This will allow user to be granted a coin.
	void authenticate();
	void reject();

};

#endif
