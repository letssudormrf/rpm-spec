ihavee-rpm
==========

Spec and source file to build rpms

1. download package source file to SOURCES directory
2. mv spec to SPECS directory
3. mv other files to SOURCES directory

and then

    spectool -R -g /path/PROJECT.spec
    rpmbuild -bb /path/PROJECT.spec

The spec has been tested only on EL6 with the EPEL repo enabled, but should also work on recent Fedoras, too.

You may need to modify version in the spec file
