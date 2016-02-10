cmake_minimum_required(VERSION 2.6)
add_library(Mux 
	Mux.cpp)
include_directories("${PROJECT_BINARY_DIR}/include/utility")
include_directories("${PROJECT_BINARY_DIR}/include/mux")
include_directories("${PROJECT_BINARY_DIR}/lib/libstatgen/include")
include_directories("${PROJECT_BINARY_DIR}/lib/cryptopp563")
target_link_libraries(Mux ${PROJECT_BINARY_DIR}/lib/cryptopp563/libcryptopp.a)
