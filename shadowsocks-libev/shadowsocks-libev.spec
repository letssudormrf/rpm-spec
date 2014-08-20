Name:           shadowsocks-libev
Version:	1.4.6
Release:	1%{?dist}
License:	GPL-3
Summary:	a lightweight secured scoks5 proxy for embedded devices and low end boxes.
Url:		https://github.com/madeye/shadowsocks-libev
Group:		Applications/Internet
Source0:	https://github.com/madeye/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:	%{name}.json
Source2:	%{name}
Packager:	Havanna <registerdedicated(at)gmail.com>
BuildRequires:	autoconf libtool gcc openssl-devel
BuildRoot: 	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXX)

%description
shadowsocks-libev is a lightweight secured scoks5 proxy for embedded devices and low end boxes.

%prep
%setup -q

%build
%configure --prefix=%{_prefix}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

install -d %{buildroot}%{_sysconfdir}
install -m 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}

install -d %{buildroot}%{_initddir}
install -m 644 %{SOURCE2} %{buildroot}/%{_initddir}

%files
%defattr(-,root,root)
%doc Changes README.md COPYING LICENSE
%config %{_sysconfdir}/shadowsocks-libev.json
%config %{_initddir}/shadowsocks-libev
%{_bindir}/ss-local
%{_bindir}/ss-redir
%{_bindir}/ss-server
%{_bindir}/ss-tunnel
%{_mandir}/man8/shadowsocks.8.gz

%changelog
