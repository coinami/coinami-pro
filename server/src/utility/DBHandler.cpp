
#include "DBHandler.h"
#include <ctime>
#include <string>

using namespace std;

inline const char * const bts(bool b) //bool to string
{
  return b ? "true" : "false";
}

int DBHandler::newGroupID(){ //creates a new grp
	char query[1024];
	sprintf(query,"insert into fastq_file_group values(DEFAULT,%ld,false,false) returning group_id",time(0));
	PGresult *result = runQuery(query);
	if(result == NULL)
		return -1;
	return atoi(PQgetvalue(result,0,PQfnumber(result,"group_id")));
}

int DBHandler::newFastQFile(int groupID,string readFile,bool isDecoy){ //adds new fastQ file
	char query[1024];
	sprintf(query,"insert into fastq_file values(%d,DEFAULT,'%s',%s) returning file_id",groupID,readFile.c_str(),bts(isDecoy));
	PGresult *result = runQuery(query);
	if(result == NULL)
		return -1;
	return atoi(PQgetvalue(result,0,PQfnumber(result,"file_id")));
}

int DBHandler::newJob(int groupID,string jobFile){ //adds new job
	char query[1024];
	sprintf(query,"insert into job values(%d,DEFAULT,'%s','',0,false,false,'') returning job_id",groupID,jobFile.c_str());
	PGresult *result = runQuery(query);
	if(result == NULL)
		return -1;
	return atoi(PQgetvalue(result,0,PQfnumber(result,"job_id")));
}

bool DBHandler::addResultFile(int jobID,string resultFile){
	char query[1024];
	sprintf(query,"update job set result_file = '%s' where job_id = %d",resultFile.c_str(),jobID);
	PGresult *result = runQuery(query);
	if(result == NULL)
		return false;
	return true;
}

string DBHandler::getResultFile(int jobID){
	char query[1024];
	sprintf(query,"select result_file from job where job_id = %d",jobID);
	PGresult *result = runQuery(query);
	if(result == NULL)
		return string();
	return string(PQgetvalue(result,0,PQfnumber(result,"result_file")));
}

int DBHandler::getIncompleteJob(){
	char query[1024];
	sprintf(query,"select job_id from job where completed = false and expiration < %ld",time(0));
	PGresult *result = runQuery(query);
	if(result == NULL)
		return -1;
	return atoi(PQgetvalue(result,0,PQfnumber(result,"job_id")));
}

bool DBHandler::assignJob(int jobID,string publicKey){
	char query[1024];
	sprintf(query,"update job set assigned_to = '%s', expiration = %ld where job_id = %d",publicKey.c_str(),time(0)+86400,jobID);
	PGresult *result = runQuery(query);
	if(result == NULL)
		return false;
	return true;
}

bool DBHandler::unassignJob(int jobID){
	char query[1024];
	sprintf(query,"update job set assigned_to = '%s', expiration = %d where job_id = %d","",0,jobID);
	PGresult *result = runQuery(query);
	if(result == NULL)
		return false;
	return true;
}

bool DBHandler::completeJob(int jobID){
	char query[1024];
	sprintf(query,"update job set completed = true where job_id = %d",jobID);
	PGresult *result = runQuery(query);
	if(result == NULL)
		return false;
	return true;
}

int DBHandler::getCompleteJob(){
	char query[1024];
	sprintf(query,"select job_id from job where completed = true and rewarded = false");
	PGresult *result = runQuery(query);
	if(result == NULL)
		return -1;
	return atoi(PQgetvalue(result,0,PQfnumber(result,"job_id")));
}

string DBHandler::getPublicKey(int jobID){
	char query[1024];
	sprintf(query,"select assigned_to from job where job_id = %d",jobID);
	PGresult *result = runQuery(query);
	if(result == NULL)
		return string();
	return string(PQgetvalue(result,0,PQfnumber(result,"assigned_to")));
}

bool DBHandler::rewardJob(int jobID){
	char query[1024];
	sprintf(query,"update job set rewarded = true where job_id = %d",jobID);
	PGresult *result = runQuery(query);
	if(result == NULL)
		return false;
	return true;
}

int DBHandler::fetchCompleteGroup(){
	char query[1024];
	sprintf(query,"select group_id from fastq_file_group where (SELECT COUNT(*) from job WHERE job.group_id = fastq_file_group.group_id and job.completed = false) = 0 and merged = false");
	PGresult *result = runQuery(query);
	if(result == NULL)
		return -1;
	return atoi(PQgetvalue(result,0,PQfnumber(result,"group_id")));
}

bool DBHandler::mergeGroup(int groupID){
	char query[1024];
	sprintf(query,"update fastq_file_group set merged = true where group_id = %d",groupID);
	PGresult *result = runQuery(query);
	if(result == NULL)
		return false;
	return true;
}

PGresult *DBHandler::runQuery(string query){
	PGresult *result = PQexec(connection,query.c_str());
	if(PQresultStatus(result) != PGRES_TUPLES_OK && PQresultStatus(result) != PGRES_COMMAND_OK){
		printf("Query failed!\n");
		printf("%s",PQerrorMessage(connection));
		return NULL;
	}
	return result;
}

bool DBHandler::connect(string connectionString){
	connection = PQconnectdb(connectionString.c_str());
	if(PQstatus(connection) != CONNECTION_OK){
		printf("Database connection failed!\n");
		return false;
	}
	return true;
}
