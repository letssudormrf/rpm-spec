Name:			shadowsocks-libev
Version:		3.0.8
Release:		1%{?dist}
Summary:		A lightweight and secure socks5 proxy

Group:			Applications/Internet
License:		GPLv3+
URL:			https://github.com/shadowsocks/%{name}
Source0:		%{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
AutoReq:		no
Conflicts:		python-shadowsocks python3-shadowsocks
BuildRequires:	autoconf, automake, asciidoc, make, gawk, gcc, gettext, libev-devel, libsodium-devel >= 1.0.4, libtool, mbedtls-devel, pcre-devel, pkgconfig, udns-devel, xmlto, zlib-devel
Requires:		libev, libsodium >= 1.0.4, mbedtls, pcre, udns, zlib

%if 0%{?fedora} >= 15 || 0%{?rhel} >=7 || 0%{?suse_version} >= 1210
%global use_systemd 1
%else
%global use_systemd 0
%endif

%if 0%{?use_systemd}
%{?systemd_requires}
%if 0%{?suse_version}
BuildRequires:	systemd-rpm-macros
%else
BuildRequires:	systemd
%endif
%endif

%description
shadowsocks-libev is a lightweight secured scoks5 proxy for embedded devices and low end boxes.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/etc/shadowsocks-libev
%if ! 0%{?use_systemd}
mkdir -p %{buildroot}%{_initddir}
install -m 755 %{_builddir}/%{buildsubdir}/rpm/SOURCES/etc/init.d/shadowsocks-libev %{buildroot}%{_initddir}/shadowsocks-libev
%else
mkdir -p %{buildroot}%{_sysconfdir}/default
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{_builddir}/%{buildsubdir}/debian/shadowsocks-libev.default %{buildroot}%{_sysconfdir}/default/shadowsocks-libev
install -m 644 %{_builddir}/%{buildsubdir}/debian/shadowsocks-libev.service %{buildroot}%{_unitdir}/shadowsocks-libev.service
install -m 644 %{_builddir}/%{buildsubdir}/debian/shadowsocks-libev-*.service %{buildroot}%{_unitdir}/
%endif
install -m 644 %{_builddir}/%{buildsubdir}/debian/config.json %{buildroot}%{_sysconfdir}/shadowsocks-libev/config.json
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions/
install -m 644 %{_builddir}/%{buildsubdir}/completions/bash/* %{buildroot}%{_datadir}/bash-completion/completions/

%pre
%if 0%{?use_systemd} && 0%{?suse_version}
%service_add_pre shadowsocks-libev.service
%endif

%post
%if ! 0%{?use_systemd}
/sbin/chkconfig --add shadowsocks-libev > /dev/null 2>&1 || :
%else
%if 0%{?suse_version}
%service_add_post shadowsocks-libev.service
%else
%systemd_post shadowsocks-libev.service
%endif
%endif

%preun
%if ! 0%{?use_systemd}
if [ $1 -eq 0 ]; then
    /sbin/service shadowsocks-libev stop  > /dev/null 2>&1 || :
    /sbin/chkconfig --del shadowsocks-libev > /dev/null 2>&1 || :
fi
%else
%if 0%{?suse_version}
%service_del_preun shadowsocks-libev.service
%else
%systemd_preun shadowsocks-libev.service
%endif
%endif

%postun
%if 0%{?use_systemd}
%if 0%{?suse_version}
%service_del_postun shadowsocks-libev.service
%else
%systemd_postun_with_restart shadowsocks-libev.service
%endif
%endif

%files
%{_docdir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/shadowsocks-libev/config.json
%{_datadir}/bash-completion/completions/*
%if ! 0%{?use_systemd}
%{_initddir}/shadowsocks-libev
%else
%{_unitdir}/shadowsocks-libev.service
%{_unitdir}/shadowsocks-libev-*.service
%config(noreplace) %{_sysconfdir}/default/shadowsocks-libev
%endif

%package devel
Summary:	Development files for shadowsocks-libev
Group:		Applications/Internet
License:	GPLv3+
Requires:	shadowsocks-libev == %{version}-%{release}

%description devel
Development files for shadowsocks-libev

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/libshadowsocks-libev.la
%{_libdir}/libshadowsocks-libev.a

%changelog
