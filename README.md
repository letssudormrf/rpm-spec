rpm-spec
========

- dnscrypt-wrapper ![](https://copr.fedorainfracloud.org/coprs/registe/dnscrypt/package/dnscrypt-wrapper/status_image/last_build.png)
- libsodium ![](https://copr.fedorainfracloud.org/coprs/registe/shadowsocks/package/libsodium/status_image/last_build.png)
- shadowsocks-libev ![](https://copr.fedorainfracloud.org/coprs/registe/shadowsocks/package/shadowsocks-libev/status_image/last_build.png)
- simple-obfs ![](https://copr.fedorainfracloud.org/coprs/registe/shadowsocks/package/simple-obfs/status_image/last_build.png)

The spec has been tested only on Centos 7 and later.

You need to install **epel-release**

    yum install epel-release
    yum install yum-plugin-copr
    yum copr enable giste/shadowsocks
    yum install shadowsocks-libev simple-obfs
