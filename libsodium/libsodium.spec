Name:           libsodium
Version:        1.0.11
Release:        1%{?dist}
Summary:        The Sodium crypto library
License:        ISC
URL:            http://libsodium.org/
Source0:        http://download.libsodium.org/libsodium/releases/%{name}-%{version}.tar.gz

%description
Sodium is a new, easy-to-use software library for encryption, decryption, 
signatures, password hashing and more. It is a portable, cross-compilable, 
installable, packageable fork of NaCl, with a compatible API, and an extended 
API to improve usability even further. Its goal is to provide all of the core 
operations needed to build higher-level cryptographic tools. The design 
choices emphasize security, and "magic constants" have clear rationales.

The same cannot be said of NIST curves, where the specific origins of certain 
constants are not described by the standards. And despite the emphasis on 
higher security, primitives are faster across-the-board than most 
implementations of the NIST standards.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name} libraries.

%prep
%setup -q

%build
%configure --disable-static --disable-silent-rules
make %{?_smp_mflags}

%install
%make_install

find %{buildroot} -name '*.la' -delete -print

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE
%{_libdir}/libsodium.so.*

%files devel
%doc AUTHORS ChangeLog README.markdown THANKS
%doc test/default/*.{c,exp,h}
%doc test/quirks/quirks.h
%{_includedir}/sodium.h
%{_includedir}/sodium/
%{_libdir}/libsodium.so
%{_libdir}/pkgconfig/libsodium.pc

%changelog
