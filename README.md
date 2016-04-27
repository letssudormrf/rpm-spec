ihavee-rpm
==========

- dnscrypt-proxy
- nginx
    - ngx_http_google_filter_module
    - ngx_http_substitutions_filter_module
- shadowsocks-libev

Spec and source file to build rpms

    echo "%_topdir %(echo $HOME)/rpmbuild" >> ~/.rpmmacros
    mkdir -p ~/rpmbuild/{BUILD,RPMS,S{OURCE,PEC,RPM}S}

mv files (exclude spec file) to $HOME/rpmbuild/SOURCES

download source package

    spectool -R -g /path/name.spec

build rpm package

    rpmbuild -bb /path/name.spec

The spec has been tested only on Centos 6.5 and later, it should also work on recent Fedoras, too.

You may need to modify version in the spec file
