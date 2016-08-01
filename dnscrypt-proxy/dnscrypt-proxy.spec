%define dnscrypt_user dnscrypt
%define dnscrypt_group dnscrypt

Name:           dnscrypt-proxy
Version:        1.7.0
Release:        1%{?dist}
Summary:        A tool for securing communications between a client and a DNS resolver.
License:        ISC
URL:            http://dnscrypt.org/
Source0:        https://download.dnscrypt.org/%{name}/%{name}-%{version}.tar.bz2
Source1:        %{name}
Source2:        %{name}.service
Packager:       Register <registerdedicated(at)gmail.com>
BuildRequires:  libsodium-devel
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXX)

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
BuildRequires:  systemd-units
Requires:       systemd
%endif

%description
The DNSCrypt daemon acts as a DNS proxy between a regular client, like
a DNS cache or an operating system stub resolver, and a DNSCrypt-aware
resolver.

%prep
%setup -q -n %{name}-%{version}

%build
./configure \
--enable-plugins \
--enable-plugins-root \
--libdir=%{_libdir} \
--prefix=%{_prefix}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
    install -d %{buildroot}%{_unitdir}
    install -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}
%endif

%files
%defattr(-,root,root)

%{_bindir}/hostip
%{_sbindir}/%{name}
%{_datadir}/%{name}
%{_includedir}/dnscrypt
%{_libdir}/%{name}
%{_mandir}/man8/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config %{_unitdir}

%pre
# Add "dnscrypt" user
getent group %{dnscrypt_group} >/dev/null || groupadd -r %{dnscrypt_group}
getent passwd %{dnscrypt_user} >/dev/null || \
    useradd -r -g %{dnscrypt_group} -s /sbin/nologin \
    -d /var/cache/dnscrypt -c "dnscrypt user"  %{dnscrypt_user}
exit 0

%post
if [ ! -d %{_localstatedir}/lib/dnscrypt ]; then
    mkdir -p %{_localstatedir}/lib/dnscrypt
    chmod %{dnscrypt_user}:%{dnscrypt_group} %{_localstatedir}/lib/dnscrypt
fi

%changelog
* Mon Aug 1 2016 Register <registerdedicated@gmail.com>
- Bump version
- 1.7.0

* Wed Apr 27 2016 Register <registerdedicated@gmail.com>
- Bump version
- 1.6.1
