%global libname libsodium
%global soname  18

Name:			libsodium
Version:		1.0.11
Release:		3%{?dist}
Summary:		The Sodium crypto library
Group:			System Environment/Libraries
License:		ISC
URL:			http://libsodium.org/
Source0:		http://download.libsodium.org/libsodium/releases/%{name}-%{version}.tar.gz

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


%package		devel
Summary:		Development files for %{name}
Requires:		%{name}%{?_isa} = %{version}-%{release}

%description	devel
This package contains libraries and header files for
developing applications that use %{name} libraries.

%package		static
Summary:		Static library for %{name}
Requires:		%{name}-devel%{?_isa} = %{version}-%{release}

%description	static
This package contains the static library for statically
linking applications to use %{name}.


%prep
%setup -q


%build
%configure \
  --disable-silent-rules \
  --disable-opt

%make_build


%install
%make_install
# for shadowsocks-libev
%if %{__isa_bits} == 64
mkdir -p %{buildroot}/usr/lib
ln -s ../..%{_libdir}/%{libname}.la %{buildroot}/usr/lib/%{libname}.la
%endif


%check
make check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license LICENSE
%{_libdir}/%{libname}.so.%{soname}*

%files devel
%doc AUTHORS ChangeLog README.markdown THANKS
%doc test/default/*.{c,exp,h}
%doc test/quirks/quirks.h
%{_includedir}/sodium.h
%{_includedir}/sodium/
%{_libdir}/%{libname}.a
%{_libdir}/%{libname}.la
%{_libdir}/%{libname}.so
%{_libdir}/pkgconfig/%{libname}.pc
%if %{__isa_bits} == 64
/usr/lib/%{libname}.la
%endif

%files static
%{_libdir}/libsodium.a

%changelog
