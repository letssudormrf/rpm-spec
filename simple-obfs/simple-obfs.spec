%global commit0 1126971c0cc4c2ee93046689440650cb56376417
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commit1 3bcb8324431d3bd4be5e4ff2a4323b455c8d5409
%global shortcommit1 %(c=%{commit0}; echo ${c:0:7})

Name:			simple-obfs
Version:		0.0.3
Release:		1%{?dist}
Summary:		A simple obfuscating tool

Group:			Applications/Internet
License:		GPLv3+
URL:			https://github.com/shadowsocks/%{name}
Source0:		https://github.com/shadowsocks/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:		https://github.com/shadowsocks/libcork/archive/%{commit1}.tar.gz#/libcork-%{shortcommit1}.tar.gz
AutoReq:		no
BuildRequires:	asciidoc, autoconf, automake, gcc, libev-devel, libtool, make, openssl, pcre-devel, udns-devel, xmlto, zlib-devel
Requires:		libev, openssl, pcre, udns, zlib


%description
Simple-obfs is a simple obfusacting tool, designed as plugin server of shadowsocks.

%prep
%autosetup -n %{name}-%{commit0} -a 1

rmdir libcork
%{__tar} xzvf %{SOURCE1}
mv -f libcork-%{commit1} libcork

%build
./autogen.sh
%configure
make %{?_smp_mflags}

%install
%make_install

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%{_docdir}/*


%changelog
