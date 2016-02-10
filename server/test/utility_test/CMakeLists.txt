cmake_minimum_required(VERSION 2.6)
add_executable(bamReader_test.exe 
	bamReader_test.cpp)
add_executable(cryptoHandler_test.exe 
	cryptoHandler_test.cpp)
add_executable(dbHandler_test.exe
	dbHandler_test.cpp)
add_executable(fastQReader_test.exe
	fastQReader_test.cpp)

include_directories("${PROJECT_BINARY_DIR}")
include_directories("${PROJECT_BINARY_DIR}/include/utility")
include_directories("${PROJECT_BINARY_DIR}/lib/libstatgen/include")
include_directories("${PROJECT_BINARY_DIR}/lib/cryptopp563")

target_link_libraries(bamReader_test.exe ${PROJECT_BINARY_DIR}/src/utility/libUtility.a)
target_link_libraries(fastQReader_test.exe ${PROJECT_BINARY_DIR}/src/utility/libUtility.a)
target_link_libraries(cryptoHandler_test.exe ${PROJECT_BINARY_DIR}/src/utility/libUtility.a)
target_link_libraries(dbHandler_test.exe ${PROJECT_BINARY_DIR}/src/utility/libUtility.a)
target_link_libraries(dbHandler_test.exe pq)

target_link_libraries(bamReader_test.exe ${PROJECT_BINARY_DIR}/lib/libstatgen/libStatGen.a)
target_link_libraries(fastQReader_test.exe ${PROJECT_BINARY_DIR}/lib/libstatgen/libStatGen.a)
target_link_libraries(cryptoHandler_test.exe ${PROJECT_BINARY_DIR}/lib/cryptopp563/libcryptopp.a)
target_link_libraries(bamReader_test.exe z)
target_link_libraries(fastQReader_test.exe z)

