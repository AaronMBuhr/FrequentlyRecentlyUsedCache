# Simple Makefile for FRUCache C++ implementation

CXX = g++
CXXFLAGS = -std=c++17 -O2 -Wall
TARGET = fru_cache_test
SRC = ../src/cpp/fru_cache.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)