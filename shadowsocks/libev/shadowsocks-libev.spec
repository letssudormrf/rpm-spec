%if 0%{?fedora} >= 15 || 0%{?rhel} >=7 || 0%{?suse_version} >= 1210
%global use_systemd 1
%else
%global use_systemd 0
%endif

Name:           shadowsocks-libev
Version:        3.1.0
Release:        1%{?dist}
Summary:        A lightweight and secure socks5 proxy

Group:          Applications/Internet
License:        GPLv3+
URL:            https://github.com/shadowsocks/%{name}
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  asciidoc automake c-ares-devel gcc libev-devel libsodium-devel >= 1.0.4 libtool make mbedtls-devel openssl-devel pcre-devel xmlto

%if 0%{?suse_version}
BuildRequires:  libopenssl-devel
%endif

%if 0%{?use_systemd}
%{?systemd_requires}
%if 0%{?suse_version}
BuildRequires:   systemd-rpm-macros
%else
BuildRequires:   systemd
%endif
%endif

AutoReq:         no
Conflicts:       python-shadowsocks python3-shadowsocks
Requires:        c-ares libev libsodium >= 1.0.4 mbedtls openssl pcre

%if 0%{?fedora} || 0%{?rhel}
Requires:        libcap
%endif
%if 0%{?suse_version}
Requires:        libcap-progs
%endif

%description
shadowsocks-libev is a lightweight secured scoks5 proxy for embedded devices and low end boxes.

%prep
%setup -q

%build
%configure --enable-shared --enable-system-shared-lib
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/etc/shadowsocks-libev
%if ! 0%{?use_systemd}
mkdir -p %{buildroot}%{_initddir}
install -m 755 %{_builddir}/%{buildsubdir}/rpm/SOURCES/etc/init.d/shadowsocks-libev %{buildroot}%{_initddir}/shadowsocks-libev
%else
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{_builddir}/%{buildsubdir}/rpm/SOURCES/systemd/shadowsocks-libev.default %{buildroot}%{_sysconfdir}/sysconfig/shadowsocks-libev
install -m 644 %{_builddir}/%{buildsubdir}/rpm/SOURCES/systemd/shadowsocks-libev*.service %{buildroot}%{_unitdir}/
%endif
install -m 644 %{_builddir}/%{buildsubdir}/debian/config.json %{buildroot}%{_sysconfdir}/shadowsocks-libev/config.json

mkdir -p %{buildroot}%{_datadir}/bash-completion/completions/
install -m 644 %{_builddir}/%{buildsubdir}/completions/bash/* %{buildroot}%{_datadir}/bash-completion/completions/
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions/
install -m 644 %{_builddir}/%{buildsubdir}/completions/zsh/* %{buildroot}%{_datadir}/zsh/site-functions/

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
setcap cap_net_bind_service+ep %{_bindir}/ss-local \
       cap_net_bind_service,cap_net_admin+ep %{_bindir}/ss-redir \
       cap_net_bind_service+ep %{_bindir}/ss-server \
       cap_net_bind_service+ep %{_bindir}/ss-tunnel

%preun
%if ! 0%{?use_systemd}
if [ $1 -eq 0 ]; then
    /sbin/service shadowsocks-libev stop  > /dev/null 2>&1 || :
    /sbin/chkconfig --del shadowsocks-libev > /dev/null 2>&1 || :
fi
%else
%if 0%{?suse_version}
%service_del_preun shadowsocks-libev.service
%service_del_preun shadowsocks-libev-local.service
%else
%systemd_preun shadowsocks-libev.service
%systemd_preun shadowsocks-libev-local.service
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    systemctl stop shadowsocks-libev-server@'*'.service  > /dev/null 2>&1 || :
    systemctl stop shadowsocks-libev-local@'*'.service  > /dev/null 2>&1 || :
    systemctl stop shadowsocks-libev-tunnel@'*'.service  > /dev/null 2>&1 || :
    systemctl stop shadowsocks-libev-redir@'*'.service  > /dev/null 2>&1 || :
    systemctl --no-reload disable shadowsocks-libev-server@.service  > /dev/null 2>&1 || :
    systemctl --no-reload disable shadowsocks-libev-local@.service  > /dev/null 2>&1 || :
    systemctl --no-reload disable shadowsocks-libev-tunnel@.service  > /dev/null 2>&1 || :
    systemctl --no-reload disable shadowsocks-libev-redir@.service  > /dev/null 2>&1 || :
fi
%endif
%endif

%postun
%if 0%{?use_systemd}
%if 0%{?suse_version}
%service_del_postun shadowsocks-libev.service
%else
%systemd_postun_with_restart shadowsocks-libev.service
%systemd_postun_with_restart shadowsocks-libev-local.service
%systemd_postun_with_restart shadowsocks-libev-server@'*'.service
%systemd_postun_with_restart shadowsocks-libev-local@'*'.service
%systemd_postun_with_restart shadowsocks-libev-tunnel@'*'.service
%systemd_postun_with_restart shadowsocks-libev-redir@'*'.service
%endif
%endif

%files
%doc %{_docdir}/shadowsocks-libev/*.html
%exclude %{_docdir}/shadowsocks-libev/ss-nat.html
%{_bindir}/*
%exclude %{_bindir}/ss-nat
%config(noreplace) %{_sysconfdir}/shadowsocks-libev/config.json
%{_datadir}/bash-completion/completions/*
%doc %{_mandir}/man*/*
%exclude %{_mandir}/man1/ss-nat.1.*
%if ! 0%{?use_systemd}
%{_initddir}/shadowsocks-libev
%else
%{_unitdir}/shadowsocks-libev*.service
%config(noreplace) %{_sysconfdir}/sysconfig/shadowsocks-libev
%endif


%package -n libshadowsocks-libev
Summary:        %{?summary} (shared library)
AutoReq:        no
Requires:       pcre openssl mbedtls libsodium >= 1.0.4 libev c-ares

%description -n libshadowsocks-libev
Shared library powered by shadowsocks-libev.

%files -n libshadowsocks-libev
%{_libdir}/*.so.*

%post -n libshadowsocks-libev
/sbin/ldconfig

%postun -n libshadowsocks-libev
/sbin/ldconfig


%package -n libshadowsocks-libev-devel
Summary:    Development files for shadowsocks-libev
Provides:   shadowsocks-libev-devel = %{version}-%{release}
Requires:   libshadowsocks-libev = %{version}-%{release}
Obsoletes:  shadowsocks-libev-devel < %{version}-%{release}

%description -n libshadowsocks-libev-devel
Development files for libshadowsocks-libev.

%files -n libshadowsocks-libev-devel
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libshadowsocks-libev.la
%{_libdir}/libshadowsocks-libev.so

%package zsh-completion
Summary:        This package installs zsh completion files for shadowsocks-libev.
Requires:       zsh shadowsocks-libev = %{version}-%{release}

%description zsh-completion
zsh completion files for shadowsocks-libev.

%files zsh-completion
%{_datadir}/zsh/site-functions/*

%changelog
