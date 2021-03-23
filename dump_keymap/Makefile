CXXFLAGS=-std=c++17 -O2 -Wall -fPIC $(shell pkg-config --cflags Qt5Gui)
LDFLAGS=$(shell pkg-config --libs Qt5Gui) 

BINS=dump_keymap

all: $(BINS)

dump_keymap: dump_keymap.o keymap.o
	$(CXX) $^ -o $@ $(LDFLAGS)

clean:
	rm -f $(BINS) *.o
