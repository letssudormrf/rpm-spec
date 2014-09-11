%global commit d37f8d302532a8d442233d9b752324ffff99bbd0
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		shadowsocks-libev
Version:	1.4.7
Release:	1%{?dist}
License:	GPL-3
Summary:	a lightweight secured scoks5 proxy for embedded devices and low end boxes.
Url:		https://github.com/madeye/%{name}
Group:		Applications/Internet
Source0:	%{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source1:	%{name}.json
Source2:	ss-local.service
Source3:	ss-server.service
Source4:	%{name}
Packager:	Havanna <registerdedicated(at)gmail.com>
BuildRequires:	autoconf libtool gcc openssl-devel
BuildRoot: 	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXX)

%description
shadowsocks-libev is a lightweight secured scoks5 proxy for embedded devices and low end boxes.

%prep
%setup -qn %{name}-%{commit}

%build
export CFLAGS="-O2"
%configure --prefix=%{_prefix}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

install -d %{buildroot}%{_sysconfdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}

%if 0%{?rhel} >= 7
	install -d %{buildroot}%{_unitdir}
	install -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}
	install -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}
%endif

%if 0%{?rhel} < 7
	install -d %{buildroot}%{_initddir}
	install -m 0755 %{SOURCE4} %{buildroot}%{_initddir}
%endif

%if 0%{?rhel} < 7
%post
/sbin/chkconfig --add %{name}
%preun
if [ $1 = 0 ]; then
	/sbin/service %{name} stop
	/sbin/chkconfig --del %{name}
fi
%endif

%files
%defattr(-,root,root)
%doc Changes README.md COPYING LICENSE
%config %{_sysconfdir}/shadowsocks-libev.json

%{_bindir}/ss-local
%{_bindir}/ss-redir
%{_bindir}/ss-server
%{_bindir}/ss-tunnel
%{_mandir}/man8/shadowsocks.8.gz

%if 0%{?rhel} >= 7
	%config %{_unitdir}/ss-local.service
	%config %{_unitdir}/ss-server.service
%endif

%if 0%{?rhel} < 7
	%config %{_initddir}/shadowsocks-libev
%endif

%changelog
