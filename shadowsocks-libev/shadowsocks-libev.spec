Name:		shadowsocks-libev
Version:	2.5.6
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
BuildRequires:	asciidoc autoconf libtool gcc openssl-devel xmlto
BuildRoot: 	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXX)

Requires:       openssl

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
%doc %{_docdir}/*
%config(noreplace) %{_sysconfdir}

%{_includedir}
%{_libdir}/*
%{_bindir}/*
%{_mandir}/*

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
