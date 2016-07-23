%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

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

BuildRequires:  systemd

%description
A simple Qubes RPC endpoint which implements a dead man's switch by responding to
triggers by locking the screen, erasing disk crypto keys, wiping main memory, and
rebooting.

%package timeout
Summary:    Lock screen timeout dead man's switch
BuildRequires:  systemd

%description timeout
A simple dead man's switch implemented with a lock screen timeout: if the system lock
screen is active longer than a certain duration, the dead man's switch is triggered.

%package bluetooth
Summary:    Bluetooth device proximity dead man's switch
Requires:  bluez pybluez
BuildRequires:  systemd

%description bluetooth
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
/usr/libexec/qubes/dom0-dms-activate
/usr/libexec/qubes/mem-wiper
/etc/qubes-rpc/qubes.DeadMansSwitch
%attr(0664,root,qubes) %config(noreplace) /etc/qubes-rpc/policy/qubes.DeadMansSwitch

%files timeout
%doc README.md
%defattr(-,root,root,-)
/usr/lib/systemd/user/qubes-app-dms-timeout.service
/usr/libexec/qubes/heartbeat
/usr/libexec/qubes/qubes-app-dms-timeout.sh

%files bluetooth
%doc README.md
%defattr(-,root,root,-)
/usr/lib/systemd/user/qubes-app-dms-bluetooth.service
/rw/usrlocal/etc/qubes-dms/bluetooth.conf
/usr/libexec/qubes/qubes-app-dms-bluetooth.py

%changelog

