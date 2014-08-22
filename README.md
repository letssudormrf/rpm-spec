ihavee-rpm
==========

Spec and source file to build rpms


mv files (exclude spec file) to SOURCES directory

and then

    spectool -R -g /path/name.spec
    rpmbuild -bb /path/name.spec

The spec has been tested only on EL6 with the EPEL repo enabled, but should also work on recent Fedoras, too.

You may need to modify version in the spec file
