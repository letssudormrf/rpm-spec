%global commit e9a530f9dcd3d94e8dcbd341b5e0ccd5bc71cd95
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           shadowsocks-libev
Version:	1.4.6
Release:	1%{?dist}
License:	GPL-3
Summary:	a lightweight secured scoks5 proxy for embedded devices and low end boxes.
Url:		https://github.com/madeye/%{name}
Group:		Applications/Internet
Source0:	%{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source1:	%{name}.json
Source2:	ss-local.service
Source3:	ss-server.service
Packager:	Havanna <registerdedicated(at)gmail.com>
BuildRequires:	autoconf libtool gcc openssl-devel
BuildRoot: 	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXX)

%description
shadowsocks-libev is a lightweight secured scoks5 proxy for embedded devices and low end boxes.

%prep
%setup -qn %{name}-%{commit}

%build
%configure --prefix=%{_prefix}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

install -d %{buildroot}%{_sysconfdir}
install -m 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}

install -d %{buildroot}%{_unitdir}
install -m 644 %{SOURCE2} %{buildroot}/%{_unitdir}
install -m 644 %{SOURCE3} %{buildroot}/%{_unitdir}

%files
%defattr(-,root,root)
%doc Changes README.md COPYING LICENSE
%config %{_sysconfdir}/shadowsocks-libev.json
%config %{_unitdir}/ss-local.service
%config %{_unitdir}/ss-server.service
%{_bindir}/ss-local
%{_bindir}/ss-redir
%{_bindir}/ss-server
%{_bindir}/ss-tunnel
%{_mandir}/man8/shadowsocks.8.gz

%changelog
