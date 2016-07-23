CFLAGS = -g -Wall -Wextra -Werror -O2 -std=c99

# See GCC bug #53229 and #64709
CFLAGS += -Wno-missing-braces -Wno-missing-field-initializers

all: mem-wiper

mem-wiper: mem-wiper.o

install:
	install -d $(DESTDIR)/usr/libexec/qubes
	install mem-wiper $(DEStDIR)/usr/libexec/qubes/mem-wiper
	install dom0-dms-activate $(DEStDIR)/usr/libexec/qubes/dom0-dms-activate

clean:
	rm -f *.o mem-wiper
