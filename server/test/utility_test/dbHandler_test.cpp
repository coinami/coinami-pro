#include<iostream>
#include<cstdlib>
#include<cstdio>
#include "DBHandler.h"

using namespace std;

int main(){
	DBHandler db;
	string connectionString = string("postgresql://amicoin:amicoin1@localhost/amicoin");
	db.connect(connectionString);

	//get new group id
	int groupID = db.newGroupID();

	printf("Group id: %d\n",groupID);
	
	//add a read
	string readFile = string("sample.fq");
	bool isDecoy = false;
	
	int fileID = db.newFastQFile(groupID,readFile,isDecoy);

	printf("File id: %d\n",fileID);

	//add a job
	string jobFile = string("job.fq");
	int jobID = db.newJob(groupID,jobFile);

	printf("Job id: %d\n",jobID);

	//assign a job to someone
	int incompleteJobID = db.getIncompleteJob();

	printf("Incomplete job id: %d\n",incompleteJobID);

	bool success = db.assignJob(incompleteJobID,string("somepublickey"));

	printf("Success assigning the job: %d\n",(int)success);
	//add result to job
	jobID = incompleteJobID;
	string resultFile = string("result.bem");
	success = db.addResultFile(jobID,resultFile);

	printf("Success adding the result: %d\n",(int)success);

	//get a result from job
	string gotFile = db.getResultFile(jobID);

	printf("Result file: %s\n",gotFile.c_str());

	//complete the job
	success = db.completeJob(jobID);

	printf("Success completing the job: %d\n",(int)success);

	//fetch a completed job (not rewarded)
	jobID = db.getCompleteJob();

	//get public key of a complete job
	string pubKey = db.getPublicKey(jobID);

	printf("Public key for a complete (not rewarded) job: %s\n",pubKey.c_str());

	//reward the pubkey
	success = db.rewardJob(jobID);

	printf("Success rewarding the job: %d\n",(int)success);

	//check for a completed group
	groupID = db.fetchCompleteGroup();

	//merge the group results
	success = db.mergeGroup(groupID);

}
