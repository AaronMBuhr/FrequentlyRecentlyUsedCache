cmake_minimum_required(VERSION 3.10)
project(FRUCache CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Set source directories
set(SRC_DIR "${PROJECT_SOURCE_DIR}/src/cpp")
set(TEST_DIR "${PROJECT_SOURCE_DIR}/tests")

# Add main cache library (as object if desired)
add_library(fru_cache OBJECT ${SRC_DIR}/fru_cache.cpp)

# Build test executable
add_executable(fru_cache_test ${TEST_DIR}/test_fru_cache.cpp $<TARGET_OBJECTS:fru_cache>)