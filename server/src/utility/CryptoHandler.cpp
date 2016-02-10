#include "CryptoHandler.h"

#include <string.h>
#include <cstdio>

using namespace CryptoPP;
using namespace std;

CryptoHandler::CryptoHandler(string keyFilePath)
{
    char* key_= getKey(keyFilePath);
    printf("key_: %s\n", key_);
    memset( key, 0x00, AES::DEFAULT_KEYLENGTH );
    memcpy( key, key_, AES::DEFAULT_KEYLENGTH );
    memset( iv, 0x00, AES::BLOCKSIZE );
    aesDecryption = AES::Decryption (key, AES::DEFAULT_KEYLENGTH);
    cbcDecryption = CBC_Mode_ExternalCipher::Decryption ( aesDecryption, iv );
    aesEncryption = AES::Encryption (key, AES::DEFAULT_KEYLENGTH);
    cbcEncryption = CBC_Mode_ExternalCipher::Encryption ( aesEncryption, iv );
}

char *CryptoHandler::getKey(string keyFilePath)
{
    FILE *f=fopen(keyFilePath.c_str(),"r");
    char *keyFromFile;
    keyFromFile = (char*) malloc(AES::DEFAULT_KEYLENGTH+2);

    if(f == NULL){
        printf("ERROR: Couldn't read the file!\n");
        strcpy(keyFromFile,"defaultkeyisthis");
        return keyFromFile;
    }
    fscanf(f,"%s",keyFromFile);
    fclose(f);
    return keyFromFile;
}

string CryptoHandler::encrypt(string plaintext){
    string ciphertext;
    cbcEncryption = CBC_Mode_ExternalCipher::Encryption ( aesEncryption, iv );
    StreamTransformationFilter stfEncryptor(cbcEncryption, new StringSink( ciphertext ) );
    stfEncryptor.Put( reinterpret_cast<const unsigned char*>( plaintext.c_str() ), plaintext.length() + 1 );
    stfEncryptor.MessageEnd();
    return encode(ciphertext);
}


string CryptoHandler::decrypt(string encodedtext){
    string decryptedtext;
    string ciphertext = decode(encodedtext);
    cbcDecryption = CBC_Mode_ExternalCipher::Decryption ( aesDecryption, iv );
    StreamTransformationFilter stfDecryptor(cbcDecryption, new StringSink( decryptedtext ) );
    stfDecryptor.Put( reinterpret_cast<const unsigned char*>( ciphertext.c_str() ), ciphertext.size() );
    stfDecryptor.MessageEnd();
    return decryptedtext;

}

string CryptoHandler::encode(string ciphertext){
   	string encoded;
	HexEncoder encoder(new StringSink(encoded));
	encoder.Put( (byte*)ciphertext.c_str(), ciphertext.size());
	encoder.MessageEnd();
	return encoded;
}

string CryptoHandler::decode(string encodedtext){
	string decoded;
	HexDecoder decoder(new StringSink(decoded));
	decoder.Put((byte*)encodedtext.c_str(), encodedtext.size());
	decoder.MessageEnd();
	return decoded;
}
