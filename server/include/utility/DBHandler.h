#ifndef DB_HANDLER_H
#define DB_HANDLER_H

#include<postgresql/libpq-fe.h>
#include<string>
using namespace std;

class DBHandler {
	public:
		int newGroupID(); //creates a new grp

		int newFastQFile(int groupID,string readFile,bool isDecoy); //adds new fastQ file

		int newJob(int groupID,string jobFile); //adds new job

		bool addResultFile(int jobID,string resultFile); //sets result file for a job

		string getResultFile(int jobID); //gets result file for a job

		int getIncompleteJob(); //returns a not completed job's ID

		bool assignJob(int jobID,string publicKey); //assigns a job to a miner
		bool unassignJob(int jobID);

		bool completeJob(int jobID); //completes a job
		int getCompleteJob(); //returns job id of a completed job

		string getPublicKey(int jobID); //returns public key of the assigned miner
		bool rewardJob(int jobID); //rewards the job

		int fetchCompleteGroup();

		bool mergeGroup(int groupID);

		bool connect(string connectionString);

	private:
		PGconn *connection;
		PGresult *runQuery(string query);
};

#endif