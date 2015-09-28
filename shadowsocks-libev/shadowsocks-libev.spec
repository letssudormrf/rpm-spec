Name:		shadowsocks-libev
Version:	2.4.0
Release:	1%{?dist}
License:	GPL-3
Summary:	a lightweight secured scoks5 proxy for embedded devices and low end boxes.
Url:		https://github.com/shadowsocks/%{name}
Group:		Applications/Internet
Source0:	%{url}/archive/v%{version}.tar.gz
Source1:	config.json
Source2:	%{name}-local@.service
Source3:	%{name}@.service
Source4:	%{name}
Packager:	Register <registerdedicated(at)gmail.com>
BuildRequires:	autoconf libtool gcc openssl-devel
BuildRoot: 	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXX)

%description
shadowsocks-libev is a lightweight secured scoks5 proxy for embedded devices and low end boxes.

%prep
%setup -q

%build
%configure --prefix=%{_prefix} --enable-shared
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

install -d %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}

%if 0%{?rhel} >= 7
	install -d %{buildroot}%{_unitdir}
	install -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}
	install -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}
%else
	install -d %{buildroot}%{_initddir}
	install -m 0755 %{SOURCE4} %{buildroot}%{_initddir}
%endif

%files
%defattr(-,root,root)
%doc Changes README.md COPYING LICENSE
%config(noreplace) %{_sysconfdir}

%{_includedir}
%{_libdir}/*
%{_bindir}/*
%{_mandir}

%if 0%{?rhel} >= 7
	%config %{_unitdir}
%else
	%config %{_initddir}
%endif

%post
if [ $1 -eq 1 ]; then
%if 0%{?rhel} >= 7
	%systemd_post %{name}@config.service
%else
	/sbin/chkconfig --add %{name}
%endif
fi

%preun
if [ $1 -eq 0 ]; then
%if 0%{?rhel} >= 7
	%systemd_preun %{name}@config.service
%else
	/sbin/service %{name} stop > /dev/null 2>&1
	/sbin/chkconfig --del %{name}
%endif
fi

%postun
%if 0%{?rhel} >= 7
%systemd_postun_with_restart %{name}@config.service
%endif

%changelog
* Mon Sep 28 2015 Register <registerdedicated(at)gmail.com> - 2.4.0
- version bump to 2.4.0

* Wed Jul 22 2015 Register <registerdedicated(at)gmail.com> - 2.3.3
- version bump to 2.3.3

* Wed Jul 22 2015 Register <registerdedicated(at)gmail.com> - 2.2.3
- version bump to 2.2.3

* Thu May 7 2015 Register <registerdedicated(at)gmail.com> - 2.2.0
- version bump to 2.2.0

* Fri Dec 19 2014 Register <registerdedicated(at)gmail.com> - 1.6.1-1
- version bump to 1.6.1

* Fri Nov 21 2014 Register <registerdedicated(at)gmail.com> - 1.5.3-1
- version bump to 1.5.3

* Fri Sep 12 2014 Register <registerdedicated(at)gmail.com> - 1.4.7-1
- version bump to 1.4.7
