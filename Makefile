CFLAGS=-O2 -Wall -Wno-deprecated-declarations
LDFLAGS=-lX11

BINS=xwsmon-ckb

all: $(BINS)

xwsmon-ckb: xwsmon-ckb.o
	$(CC) xwsmon-ckb.o -o xwsmon-ckb $(LDFLAGS)

clean:
	rm -f $(BINS) *.o
