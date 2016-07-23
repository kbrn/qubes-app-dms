install:
	install -d $(DESTDIR)/etc/qubes-rpc
	install -m 0644 qubes.DeadMansSwitch $(DESTDIR)/etc/qubes-rpc
	install -m 0664 -D policy/qubes.DeadMansSwitch \
		$(DESTDIR)/etc/qubes-rpc/policy/qubes.DeadMansSwitch
	install -m 0644 qubes-app-dms-timeout.service $(DESTDIR)/usr/lib/systemd/user/qubes-app-dms-timeout.service

