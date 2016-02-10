#include "FastQSequence.h"

void FastQSequence::print(){
	cout<<sequenceIdLine <<endl;
	cout<<rawSequence<<endl;
	cout<<plusLine<<endl;
	cout<<qualityString<<endl;
	return;
}