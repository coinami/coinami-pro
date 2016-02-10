cmake_minimum_required(VERSION 2.6)
add_library(Demux 
	Demux.cpp)
include_directories("${PROJECT_BINARY_DIR}/include/utility")
include_directories("${PROJECT_BINARY_DIR}/include/demux")
include_directories("${PROJECT_BINARY_DIR}/lib/libstatgen/include")
include_directories("${PROJECT_BINARY_DIR}/lib/cryptopp563")
target_link_libraries(Demux ${PROJECT_BINARY_DIR}/lib/cryptopp563/libcryptopp.a)
