Name:			dnscrypt-wrapper
Version:		0.2.2
Release:		1%{?dist}
Summary:		DNSCrypt server

Group:			System Environment/Daemons
License:		ISC
URL:			http://dnscrypt.org/
Source0:		https://github.com/Cofyc/%{name}/archive/v%{version}.tar.gz

BuildRequires:	autoconf libevent-devel libsodium-devel

%description
DNSCrypt is a protocol that authenticates communications between a DNS
client and a DNS resolver. It prevents DNS spoofing. It uses cryptographic
signatures to verify that responses originate from the chosen DNS resolver
and haven't been tampered with.

%prep
%setup -q

%build
make configure
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%{_sbindir}/*

%changelog
