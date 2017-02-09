ihavee-rpm
==========

- dnscrypt-proxy
- libsodium
- shadowsocks-libev
- simple-obfs

Spec and source file to build rpms

    echo "%_topdir %(echo $HOME)/rpmbuild" >> ~/.rpmmacros
    mkdir -p ~/rpmbuild/{BUILD,RPMS,S{OURCE,PEC,RPM}S}

Install build tools

    yum install rpm-build rpmdevtools

Download source package

    spectool -R -g /path/name.spec

Build rpm package

    rpmbuild -bb /path/name.spec

You need to install BuildRequires package from name.spec

The spec has been tested only on Centos 7 and later, it should also work on recent Fedoras too.

You may need to modify version in the spec file, and you may need to install **epel-release**

    yum install epel-release
