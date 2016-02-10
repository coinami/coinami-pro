#include<iostream>
#include "CryptoHandler.h"
using namespace std;

int main(){
	CryptoHandler handler("here_is_the_key.aham");
	while(true){
		string cipher = handler.encrypt("ahmet");
		cout << "cipher:" << cipher << endl;
		string plain = handler.decrypt(cipher);
		cout << "plain :" << plain << endl;
	}
	return 0;
}
