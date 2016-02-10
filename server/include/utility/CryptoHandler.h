#ifndef CRYPTO_HANDLER_H
#define CRYPTO_HANDLER_H

#include <string>
#include <cstdio>
#include "modes.h"
#include "aes.h"
#include "filters.h"
#include "hex.h"


using namespace std;
using namespace CryptoPP;

class CryptoHandler {
	public:
		CryptoHandler(string keyFilePath);
		string decrypt(string plaintext);
		//This method will decrypt a data with asymmetric encryption.
		string encrypt(string ciphertext);
		//This method will encrypt a data with asymmetric encryption.
	private:
		byte key[ AES::DEFAULT_KEYLENGTH ], iv[ AES::BLOCKSIZE ];
        CBC_Mode_ExternalCipher::Decryption cbcDecryption;
        CBC_Mode_ExternalCipher::Encryption cbcEncryption;
        AES::Decryption aesDecryption;
        AES::Encryption aesEncryption;
        string encode(string ciphertext);
        string decode(string encodedtext);
        char* getKey(string keyFilePath);
};

#endif
