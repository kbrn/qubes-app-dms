CFLAGS = -g -Wall -Wextra -Werror -O2 -std=c99

# See GCC bug #53229 and #64709
CFLAGS += -Wno-missing-braces -Wno-missing-field-initializers

all: mem-wiper heartbeat

mem-wiper: mem-wiper.o
heartbeat: heartbeat.o

install:
	install -d $(DESTDIR)/usr/libexec/qubes
	install mem-wiper $(DESTDIR)/usr/libexec/qubes/mem-wiper
	install heartbeat $(DESTDIR)/usr/libexec/qubes/heartbeat
	install qubes-app-dms-timeout.sh $(DESTDIR)/usr/libexec/qubes/qubes-app-dms-timeout.sh
	install dom0-dms-activate $(DESTDIR)/usr/libexec/qubes/dom0-dms-activate

clean:
	rm -f *.o mem-wiper heartbeat
