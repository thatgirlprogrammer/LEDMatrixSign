DIR=$(DESTDIR)/opt/LEDMatrixSign
#DIR= .
LIBDIR=$(DESTDIR)/usr/lib

COMPILELIBDIR=./lib

all: LEDMatrixSign

.PHONY: all install clean distclean

LEDMatrixSign: sign2.py
	export LIBRARY_PATH=$(COMPILELIBDIR):$(LIBRARY_PATH)
	chmod +x sign2.py

install: LEDMatrixSign
	mkdir -p $(LIBDIR)
	mkdir -p $(DIR)
	install sign2.py $(DIR)/sign2.py
	install samplebase.py $(DIR)/samplebase.py
	install signContent.txt $(DIR)/signContent.txt
	install sign.init /etc/init.d/LEDMatrixSign
	cp README.md $(DIR)/README
	update-rc.d LEDMatrixSign defaults

clean:
	rm -f LEDMatrixSign
