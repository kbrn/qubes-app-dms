%define version %(cat version)
%if 0%{?qubes_builder}
%define _builddir %(pwd)
%endif
    
Name:		qubes-app-dms
Version:	%{version}
Release:	1%{?dist}
Summary:	Dead man's switch (receiver)

Group:		System Environment/Daemons
License:	GPLv2
URL:		https://www.qubes-os.org/

%description
A simple Qubes RPC endpoint which implements a dead man's switch by responding to
triggers by locking the screen, erasing disk crypto keys, wiping main memory, and
rebooting.

%package qubes-app-dms-timeout
Summary:    Lock screen timeout dead man's switch

%description qubes-app-dms-timeout
A simple dead man's switch implemented with a lock screen timeout: if the system lock
screen is active longer than a certain duration, the dead man's switch is triggered.

%package qubes-app-dms-bluetooth
Summary:    Bluetooth device proximity dead man's switch

%description qubes-app-dms-bluetooth
A dead man's switch implemented with a Bluetooth device's proximity.  Once a pre-
configured Bluetooth device becomes visible, regular Bluetooth discovery ensures
that device remains nearby.  If the device disappears for a specified number of
probes, the dead man's switch is triggered.

%prep
# we operate on the current directory, so no need to unpack anything
# symlink is to generate useful debuginfo packages
rm -f %{name}-%{version}
ln -sf . %{name}-%{version}
%setup -T -D

%build
make %{?_smp_mflags} all

%install
make install DESTDIR=%{buildroot}

%files
%doc README.md
%defattr(-,root,root,-)
#/usr/bin/input-proxy-receiver
#/etc/qubes-rpc/qubes.InputMouse
#/etc/qubes-rpc/qubes.InputKeyboard
#/lib/udev/rules.d/90-qubes-uinput.rules
#/lib/modules-load.d/qubes-uinput.conf
#%{python_sitelib}/qubesinputproxy-*.egg-info/*
#%{python_sitelib}/qubesinputproxy
#%attr(0664,root,qubes) %config(noreplace) /etc/qubes-rpc/policy/qubes.InputMouse
#%attr(0664,root,qubes) %config(noreplace) /etc/qubes-rpc/policy/qubes.InputKeyboard

%files qubes-app-dms-timeout
%doc README.md
%defattr(-,root,root,-)
#/usr/bin/input-proxy-sender
#/usr/bin/qubes-input-trigger
#%config(noreplace) /etc/xdg/autostart/qubes-input-trigger.desktop
#/lib/udev/rules.d/90-qubes-input-proxy.rules
#%{_unitdir}/qubes-input-sender-mouse@.service
#%{_unitdir}/qubes-input-sender-keyboard@.service
#%{_unitdir}/qubes-input-sender-keyboard-mouse@.service

%files qubes-app-dms-bluetooth
%doc README.md
%defattr(-,root,root,-)
#/usr/bin/input-proxy-sender
#/usr/bin/qubes-input-trigger
#%config(noreplace) /etc/xdg/autostart/qubes-input-trigger.desktop
#/lib/udev/rules.d/90-qubes-input-proxy.rules
#%{_unitdir}/qubes-input-sender-mouse@.service
#%{_unitdir}/qubes-input-sender-keyboard@.service
#%{_unitdir}/qubes-input-sender-keyboard-mouse@.service

%changelog

