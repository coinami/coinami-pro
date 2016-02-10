cmake_minimum_required(VERSION 2.6)
add_library(Utility 
	BamReader.cpp 
	BamWriter.cpp 
	CryptoHandler.cpp 
	DBHandler.cpp 
	FastQReader.cpp
	FastQSequence.cpp 
	FastQWriter.cpp)
include_directories("${PROJECT_BINARY_DIR}/include/utility")
include_directories("${PROJECT_BINARY_DIR}/lib/libstatgen/include")
include_directories("${PROJECT_BINARY_DIR}/lib/cryptopp563")
target_link_libraries(Utility ${PROJECT_BINARY_DIR}/lib/libstatgen/libStatGen.a)
target_link_libraries(Utility ${PROJECT_BINARY_DIR}/lib/cryptopp563/libcryptopp.a)
target_link_libraries(Utility pq)


