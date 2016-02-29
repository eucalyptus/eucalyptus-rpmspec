# Copyright 2009-2015 Eucalyptus Systems, Inc.
#
# Redistribution and use of this software in source and binary forms, with or
# without modification, are permitted provided that the following conditions
# are met:
#
#   Redistributions of source code must retain the above
#   copyright notice, this list of conditions and the
#   following disclaimer.
#
#   Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the
#   following disclaimer in the documentation and/or other
#   materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:       Eucalyptus cloud platform
Name:          eucalyptus
Version:       4.2.2
Release:       0%{?build_id:.%build_id}%{?dist}
License:       GPLv3
URL:           http://www.eucalyptus.com
Group:         Applications/System

BuildRequires: ant >= 1.7
BuildRequires: ant-nodeps >= 1.7
BuildRequires: apache-ivy
BuildRequires: axis2-adb-codegen
BuildRequires: axis2-codegen
BuildRequires: axis2c-devel >= 1.6.0
BuildRequires: curl-devel
BuildRequires: java-1.7.0-openjdk-devel >= 1:1.7.0
BuildRequires: jpackage-utils
BuildRequires: json-c-devel
BuildRequires: libuuid-devel
BuildRequires: libvirt-devel >= 0.6
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: m2crypto
BuildRequires: openssl-devel
BuildRequires: python-devel
BuildRequires: python-setuptools
BuildRequires: rampartc-devel >= 1.3.0
BuildRequires: swig
BuildRequires: xalan-j2-xsltc
BuildRequires: /usr/bin/awk

Requires(pre): shadow-utils

BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Source0:       %{tarball_basedir}.tar.xz
Source1:       %{cloud_lib_tarball}
# A version of WSDL2C.sh that respects standard classpaths
Source2:       euca-WSDL2C.sh

%description
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains bits that are shared by all Eucalyptus components
and is not particularly useful on its own -- to get a usable cloud you
will need to install Eucalyptus services as well.


%package axis2c-common
Summary:      Eucalyptus cloud platform - Axis2/C shared components
Group:        Applications/System

Requires:     %{name} = %{version}-%{release}
Requires:     httpd
Requires:     perl(Digest::MD5)
Requires:     perl(MIME::Base64)

%description axis2c-common
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains shared components used by all eucalyptus services
that are based on Axis2/C.


%package blockdev-utils
Summary:      Eucalyptus cloud platform - shared block device utilities
Group:        Applications/System

Requires:     %{name} = %{version}-%{release}
Requires:     libselinux-python
Requires:     perl(Crypt::OpenSSL::RSA)
Requires:     perl(Crypt::OpenSSL::Random)
Requires:     perl(MIME::Base64)
Requires:     /usr/bin/which

%description blockdev-utils
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains shared components used by all eucalyptus services
that connect to iSCSI targets.


%package common-java
Summary:      Eucalyptus cloud platform - ws java stack
Group:        Applications/System
Requires:     %{name} = %{version}-%{release}
Requires:     %{name}-common-java-libs = %{version}-%{release}
Requires:     lvm2
Requires:     /usr/bin/which
Requires:     %{_sbindir}/euca_conf

Obsoletes:    eucalyptus-osg < 4.0.1
Provides:     eucalyptus-osg = %{version}-%{release}

%description common-java
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the common-java files.


%package common-java-libs
Summary:      Eucalyptus cloud platform - ws java stack libs
Group:        Applications/System

Requires:     jpackage-utils
Requires:     java-1.7.0-openjdk >= 1:1.7.0

%description common-java-libs
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the java WS stack.


%package walrus
Summary:      Eucalyptus cloud platform - walrus
Group:        Applications/System

Requires:     %{name}             = %{version}-%{release}
Requires:     %{name}-common-java = %{version}-%{release}
Requires:     lvm2

%description walrus
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains storage component for your cloud: images and buckets
are handled by walrus. Typically this package is installed alongside the
cloud controller.


%package sc
Summary:      Eucalyptus cloud platform - storage controller
Group:        Applications/System

Requires:     %{name} = %{version}-%{release}
Requires:     %{name}-blockdev-utils = %{version}-%{release}
Requires:     %{name}-common-java = %{version}-%{release}
Requires:     device-mapper-multipath
Requires:     iscsi-initiator-utils
Requires:     librados2%{?_isa}
Requires:     librbd1%{?_isa}
Requires:     lvm2
Requires:     scsi-target-utils

%description sc
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the storage controller part of eucalyptus, which
handles the elastic blocks for a given cluster. Typically you install it
alongside the cluster controller.


%package cloud
Summary:      Eucalyptus cloud platform - cloud controller
Group:        Applications/System

Requires:     %{name}                     = %{version}-%{release}
Requires:     %{name}-common-java%{?_isa} = %{version}-%{release}
# bc is needed for /etc/eucalyptus/cloud.d/init.d/01_pg_kernel_params
Requires:     bc
Requires:     euca2ools >= 2.0
Requires:     eucanetd = %{version}-%{release}
Requires:     libselinux-python
Requires:     lvm2
# Older openssl had a handshake bug that fails credential download
Requires:     openssl%{?_isa} >= 1.0.1e-16
Requires:     perl(Getopt::Long)
Requires:     postgresql92
Requires:     postgresql92-server
Requires:     python-argparse
Requires:     rsync

%description cloud
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the cloud controller part of eucalyptus. The cloud
controller needs to be reachable by both the cluster controller and from
the cloud clients.


%package cc
Summary:      Eucalyptus cloud platform - cluster controller
Group:        Applications/System

Requires:     %{name} = %{version}-%{release}
Requires:     %{name}-axis2c-common = %{version}-%{release}
Requires:     bridge-utils
Requires:     dhcp >= 4.1.1-33.P1
Requires:     eucanetd = %{version}-%{release}
Requires:     httpd
Requires:     iproute
Requires:     iptables
Requires:     iputils
Requires:     libselinux-python
Requires:     python-argparse
Requires:     rsync
Requires:     vconfig
Requires:     vtun
Requires:     /usr/bin/which
Requires:     %{_sbindir}/euca_conf

%description cc
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the cluster controller part of eucalyptus. It
handles a group of node controllers.


%package nc
Summary:      Eucalyptus cloud platform - node controller
Group:        Applications/System

Requires:     %{name} = %{version}-%{release}
Requires:     %{name}-axis2c-common = %{version}-%{release}
Requires:     %{name}-blockdev-utils = %{version}-%{release}
Requires:     %{name}-imaging-toolkit = %{version}-%{release}
Requires:     bridge-utils
Requires:     device-mapper
Requires:     device-mapper-multipath
Requires:     euca2ools >= 3.2
Requires:     eucanetd = %{version}-%{release}
Requires:     httpd
Requires:     iscsi-initiator-utils
Requires:     kvm
# Ceph support requires librados2, librbd1, and *also* qemu-kvm-rhev.
Requires:     librados2%{?_isa}
Requires:     librbd1%{?_isa}
Requires:     libvirt
Requires:     perl(Sys::Virt)
Requires:     perl(Time::HiRes)
Requires:     perl(XML::Simple)
# The next six come from storage/diskutil.c, which shells out to lots of stuff.
Requires:     coreutils
Requires:     curl
Requires:     e2fsprogs
Requires:     file
Requires:     parted
Requires:     vconfig
Requires:     util-linux
Requires:     /usr/bin/which
Requires:     %{_sbindir}/euca_conf

%description nc
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the node controller part of eucalyptus. This
component handles instances.


%package admin-tools
Summary:      Eucalyptus cloud platform - admin CLI tools
# A patched version of python's gzip is included, so we add the Python license
License:      BSD and Python
Group:        Applications/System

Requires:     %{name} = %{version}-%{release}
Requires:     euca2ools >= 3.2
Requires:     m2crypto
Requires:     PyGreSQL
Requires:     python-boto >= 2.1
Requires:     python-prettytable
Requires:     python-requestbuilder >= 0.4
Requires:     python-requests
Requires:     python-six
Requires:     PyYAML
Requires:     rsync
Requires:     /usr/bin/which

BuildArch:    noarch

%description admin-tools
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains command line tools necessary for managing a
Eucalyptus cluster.


%package -n eucanetd
Summary:        Eucalyptus cloud platform - edge networking daemon
License:        GPLv3
Group:          Applications/System

Requires:       dhcp >= 4.1.1-33.P1
Requires:       ebtables
Requires:       ipset
Requires:       iptables
Requires:       /usr/bin/which

%description -n eucanetd
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the daemon that controls the edge networking mode.
To use edge networking mode, all node controllers must have this package
installed.


%package imaging-toolkit
Summary:      Eucalyptus cloud platform - image manipulation tookit
License:      ASL 2.0

Requires:     %{name} = %{version}-%{release}
# This includes both things under tools/imaging and storage.
Requires:     euca2ools >= 3.1
Requires:     pv
Requires:     python-argparse
Requires:     python-lxml
Requires:     python-requests
# The next seven come from euca-imager (storage/diskutil.c), which shells
# out to lots of stuff
Requires:     coreutils
Requires:     e2fsprogs
Requires:     file
Requires:     grub
Requires:     httpd
Requires:     parted
Requires:     util-linux

%description imaging-toolkit
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains a toolkit used internally by Eucalyptus to download
and upload virtual machine images and to convert them between formats.


%prep
%setup -q -n %{tarball_basedir}

# Filter unwanted perl provides
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
sed -e '/perl(disconnect_iscsitarget_main.pl)/d' \
    -e '/perl(connect_iscsitarget_main.pl)/d' \
    -e '/perl(iscsitarget_common.pl)/d'
EOF

%global __perl_provides %{_builddir}/%{tarball_basedir}/%{name}-prov
chmod +x %{__perl_provides}

# Filter unwanted perl requires
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
sed -e '/perl(disconnect_iscsitarget_main.pl)/d' \
    -e '/perl(connect_iscsitarget_main.pl)/d' \
    -e '/perl(iscsitarget_common.pl)/d'
EOF

%global __perl_requires %{_builddir}/%{tarball_basedir}/%{name}-req
chmod +x %{__perl_requires}


%build
export CFLAGS="%{optflags}"

# Eucalyptus does not assign the usual meaning to prefix and other standard
# configure variables, so we can't realistically use %%configure.
./configure --with-axis2=%{_datadir}/axis2-* --with-axis2c=%{axis2c_home} --with-wsdl2c-sh=%{S:2} --enable-debug --prefix=/ --with-apache2-module-dir=%{_libdir}/httpd/modules --with-db-home=/usr/pgsql-9.2 --with-extra-version=%{release}

# Untar the bundled cloud-lib Java dependencies.
mkdir clc/lib
tar xf %{SOURCE1} -C clc/lib

# Don't bother with git since we're using a cloud-libs tarball
touch clc/.nogit

# FIXME: storage/Makefile breaks with parallel make
make # %{?_smp_mflags}


%install
[ $RPM_BUILD_ROOT != "/" ] && rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

sed -i -e 's#.*EUCALYPTUS=.*#EUCALYPTUS="/"#' \
       -e 's#.*HYPERVISOR=.*#HYPERVISOR="kvm"#' \
       -e 's#.*INSTANCE_PATH=.*#INSTANCE_PATH="/var/lib/eucalyptus/instances"#' \
       -e 's#.*VNET_BRIDGE=.*#VNET_BRIDGE="br0"#' \
       $RPM_BUILD_ROOT/etc/eucalyptus/eucalyptus.conf

# Eucalyptus's build scripts do not respect initrddir
if [ %{_initrddir} != /etc/init.d ]; then
    mkdir -p $RPM_BUILD_ROOT/%{_initrddir}
    mv $RPM_BUILD_ROOT/etc/init.d/* $RPM_BUILD_ROOT/%{_initrddir}
    rmdir $RPM_BUILD_ROOT/etc/init.d
fi

# Create the directories where components store their data
mkdir -p $RPM_BUILD_ROOT/var/lib/eucalyptus
touch $RPM_BUILD_ROOT/var/lib/eucalyptus/services
for dir in bukkits CC db keys ldap upgrade vmware volumes webapps; do
    install -d -m 0700 $RPM_BUILD_ROOT/var/lib/eucalyptus/$dir
done
install -d -m 0771 $RPM_BUILD_ROOT/var/lib/eucalyptus/instances
install -d -m 0755 $RPM_BUILD_ROOT/var/run/eucalyptus/net
install -d -m 0750 $RPM_BUILD_ROOT/var/run/eucalyptus/status

# Touch httpd config files that the init scripts create so we can %ghost them
touch $RPM_BUILD_ROOT/var/run/eucalyptus/httpd-{cc,nc,tmp}.conf

# Add PolicyKit config on systems that support it
mkdir -p $RPM_BUILD_ROOT/var/lib/polkit-1/localauthority/10-vendor.d
cp -p tools/eucalyptus-nc-libvirt.pkla $RPM_BUILD_ROOT/var/lib/polkit-1/localauthority/10-vendor.d/eucalyptus-nc-libvirt.pkla

# Put udev rules in the right place
mkdir -p $RPM_BUILD_ROOT/lib/udev/rules.d
cp -p $RPM_BUILD_ROOT/usr/share/eucalyptus/udev/rules.d/12-dm-permissions.rules $RPM_BUILD_ROOT/lib/udev/rules.d/12-dm-permissions.rules
cp -p $RPM_BUILD_ROOT/usr/share/eucalyptus/udev/rules.d/55-openiscsi.rules $RPM_BUILD_ROOT/lib/udev/rules.d/55-openiscsi.rules
# FIXME:  iscsidev.sh belongs in /usr/share/eucalyptus [RT:2093]
mkdir -p $RPM_BUILD_ROOT/etc/udev/scripts
install -m 0755 $RPM_BUILD_ROOT/usr/share/eucalyptus/udev/iscsidev.sh $RPM_BUILD_ROOT/etc/udev/scripts/iscsidev.sh
rm -rf $RPM_BUILD_ROOT/usr/share/eucalyptus/udev

# Store admin tool config files
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/eucalyptus-admin
cp -Rp admin-tools/conf/* $RPM_BUILD_ROOT/%{_sysconfdir}/eucalyptus-admin

# Work around a regression in libvirtd.conf file handling that appears
# in at least RHEL 6.2
# https://www.redhat.com/archives/libvirt-users/2011-July/msg00039.html
mkdir $RPM_BUILD_ROOT/var/lib/eucalyptus/.libvirt
touch $RPM_BUILD_ROOT/var/lib/eucalyptus/.libvirt/libvirtd.conf

# Remove README file if one exists
rm -f $RPM_BUILD_ROOT/usr/share/eucalyptus/README


%files
%defattr(-,root,root,-)
%doc LICENSE INSTALL README

%attr(-,eucalyptus,eucalyptus) %dir /etc/eucalyptus
%attr(-,root,eucalyptus) %dir /usr/lib/eucalyptus
%attr(-,root,eucalyptus) %dir /usr/libexec/eucalyptus
%dir /usr/share/eucalyptus
%doc /usr/share/eucalyptus/doc/
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/keys
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/upgrade
%attr(-,eucalyptus,eucalyptus) %dir /var/log/eucalyptus
%attr(-,eucalyptus,eucalyptus) %dir /var/run/eucalyptus
%attr(-,eucalyptus,eucalyptus-status) %dir /var/run/eucalyptus/status

%config(noreplace) /etc/eucalyptus/eucalyptus.conf
/etc/eucalyptus/eucalyptus-version

# This is currently used for CC and NC httpd logs.
/etc/logrotate.d/eucalyptus

%attr(4750,root,eucalyptus) /usr/lib/eucalyptus/euca_mountwrap
%attr(4750,root,eucalyptus) /usr/lib/eucalyptus/euca_rootwrap
/usr/libexec/eucalyptus/euca-upgrade

/usr/sbin/euca-generate-fault
/usr/share/eucalyptus/faults/
/usr/share/eucalyptus/status/


%files axis2c-common
# CC and NC
/etc/eucalyptus/httpd.conf
/usr/share/eucalyptus/policies
%ghost /var/run/eucalyptus/httpd-tmp.conf
/usr/share/eucalyptus/euca_ipt
/usr/share/eucalyptus/floppy
/usr/share/eucalyptus/populate_arp.pl
%{axis2c_home}/services/EucalyptusGL/


%files blockdev-utils
# SC and NC
%doc tools/multipath.conf.example.* tools/iscsid.conf.example
/etc/udev/scripts/iscsidev.sh
/lib/udev/rules.d/12-dm-permissions.rules
/lib/udev/rules.d/55-openiscsi*.rules
/usr/share/eucalyptus/create-loop-devices
/usr/share/eucalyptus/connect_iscsitarget.pl
/usr/share/eucalyptus/connect_iscsitarget_main.pl
/usr/share/eucalyptus/connect_iscsitarget_sc.pl
/usr/share/eucalyptus/disconnect_iscsitarget.pl
/usr/share/eucalyptus/disconnect_iscsitarget_main.pl
/usr/share/eucalyptus/disconnect_iscsitarget_sc.pl
/usr/share/eucalyptus/get_iscsitarget.pl
/usr/share/eucalyptus/iscsitarget_common.pl


%files common-java
%defattr(-,root,root,-)
%{_initrddir}/eucalyptus-cloud
# cloud.d contains random stuff used by every Java component.  Most of it
# probably belongs in /usr/share, but moving it will be painful.
# https://eucalyptus.atlassian.net/browse/EUCA-11002
%dir /etc/eucalyptus/cloud.d
/etc/eucalyptus/cloud.d/conf/
%dir /etc/eucalyptus/cloud.d/elb-security-policy
%config(noreplace) /etc/eucalyptus/cloud.d/elb-security-policy/*
%dir /etc/eucalyptus/cloud.d/init.d
/etc/eucalyptus/cloud.d/jmx/
/etc/eucalyptus/cloud.d/scripts/
/etc/eucalyptus/cloud.d/security.policy
/etc/eucalyptus/cloud.d/www/
/usr/sbin/eucalyptus-cloud
%ghost /var/lib/eucalyptus/services
%attr(-,eucalyptus,eucalyptus) /var/lib/eucalyptus/webapps/


%files common-java-libs
%defattr(-,root,root,-)
/usr/share/eucalyptus/*jar*
%doc /usr/share/eucalyptus/licenses/


%files cloud
%defattr(-,root,root,-)
/etc/eucalyptus/cloud.d/init.d/01_pg_kernel_params
/usr/sbin/euca-lictool
/usr/sbin/clcadmin-*
/usr/share/eucalyptus/lic_default
/usr/share/eucalyptus/lic_template
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/db


%files walrus
%defattr(-,root,root,-)
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/bukkits


%files sc
%defattr(-,root,root,-)
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/volumes


%files cc
%defattr(-,root,root,-)
%{_initrddir}/eucalyptus-cc
%{axis2c_home}/services/EucalyptusCC/
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/CC
%ghost /var/run/eucalyptus/httpd-cc.conf
/usr/lib/eucalyptus/shutdownCC
/usr/sbin/clusteradmin-*
/usr/share/eucalyptus/vtunall.conf.template
/usr/share/eucalyptus/dynserv.pl
/usr/share/eucalyptus/getstats_net.pl


%files nc
%defattr(-,root,root,-)
%doc tools/nc-hooks
%config(noreplace) /etc/eucalyptus/libvirt.xsl
%dir /etc/eucalyptus/nc-hooks
/etc/eucalyptus/nc-hooks/example.sh
%{_initrddir}/eucalyptus-nc
%{axis2c_home}/services/EucalyptusNC/
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/instances
%ghost /var/run/eucalyptus/httpd-nc.conf
/usr/sbin/euca_test_nc
/usr/share/eucalyptus/authorize-migration-keys.pl
/usr/share/eucalyptus/detach.pl
/usr/share/eucalyptus/gen_kvm_libvirt_xml
/usr/share/eucalyptus/gen_libvirt_xml
/usr/share/eucalyptus/generate-migration-keys.sh
/usr/share/eucalyptus/getstats.pl
/usr/share/eucalyptus/get_bundle
/usr/share/eucalyptus/get_sys_info
/usr/share/eucalyptus/get_xen_info
/usr/share/eucalyptus/partition2disk
%attr(-,eucalyptus,eucalyptus) /var/lib/eucalyptus/.libvirt/
/var/lib/polkit-1/localauthority/10-vendor.d/eucalyptus-nc-libvirt.pkla


%files admin-tools
%defattr(-,root,root,-)
# Old stuff (remove after 4.2)
%{python_sitelib}/eucadmin*
%{_sbindir}/euca_conf
%{_sbindir}/euca-deregister-arbitrator
%{_sbindir}/euca-deregister-cloud
%{_sbindir}/euca-deregister-cluster
%{_sbindir}/euca-deregister-service
%{_sbindir}/euca-deregister-storage-controller
%{_sbindir}/euca-deregister-walrusbackend
%{_sbindir}/euca-describe-arbitrators
%{_sbindir}/euca-describe-autoscaling
%{_sbindir}/euca-describe-cloudformation
%{_sbindir}/euca-describe-clouds
%{_sbindir}/euca-describe-cloudwatch
%{_sbindir}/euca-describe-clusters
%{_sbindir}/euca-describe-compute
%{_sbindir}/euca-describe-components
%{_sbindir}/euca-describe-euare
%{_sbindir}/euca-describe-loadbalancing
%{_sbindir}/euca-describe-nodes
%{_sbindir}/euca-describe-object-storage-gateways
%{_sbindir}/euca-describe-properties
%{_sbindir}/euca-describe-services
%{_sbindir}/euca-describe-service-types
%{_sbindir}/euca-describe-storage-controllers
%{_sbindir}/euca-describe-tokens
%{_sbindir}/euca-describe-walrusbackends
%{_sbindir}/euca-get-credentials
%{_sbindir}/euca-migrate-instances
%{_sbindir}/euca-modify-cluster
%{_sbindir}/euca-modify-property
%{_sbindir}/euca-modify-service
%{_sbindir}/euca-modify-storage-controller
%{_sbindir}/euca-modify-walrus
%{_sbindir}/euca-register-arbitrator
%{_sbindir}/euca-register-cloud
%{_sbindir}/euca-register-cluster
%{_sbindir}/euca-register-service
%{_sbindir}/euca-register-storage-controller
%{_sbindir}/euca-register-walrusbackend
%{_sbindir}/eureport-generate-report
%{_sbindir}/eureport-export-data
%{_sbindir}/eureport-delete-data
# New stuff (new in 4.2)
%{python_sitelib}/eucalyptus_admin*
%{_bindir}/euctl
%{_bindir}/euserv-*
%{_mandir}/man1/euctl.1*
%{_mandir}/man1/euserv-*.1*
%dir %{_sysconfdir}/eucalyptus-admin
%dir %{_sysconfdir}/eucalyptus-admin/conf.d
%config(noreplace) %{_sysconfdir}/eucalyptus-admin/eucalyptus-admin.ini
%config(noreplace) %{_sysconfdir}/eucalyptus-admin/conf.d/localhost.ini


%files -n eucanetd
%defattr(-,root,root,-)
%{_libexecdir}/eucalyptus/announce-arp
%{_sbindir}/eucanetd
%{_initrddir}/eucanetd
%attr(-,eucalyptus,eucalyptus) /var/run/eucalyptus/net
%attr(0755,root,eucalyptus) /usr/libexec/eucalyptus/conntrack_kernel_params
/usr/share/eucalyptus/nginx_proxy.conf


%files imaging-toolkit
%{_libexecdir}/eucalyptus/euca-imager
%{_libexecdir}/eucalyptus/euca-run-workflow
%{python_sitelib}/eucatoolkit*


%pre
getent group eucalyptus >/dev/null || groupadd -r eucalyptus
getent group eucalyptus-status >/dev/null || groupadd -r eucalyptus-status
## FIXME:  Make QA (and Eucalyptus proper?) work with /sbin/nologin as the shell [RT:2092]
#getent passwd eucalyptus >/dev/null || \
#    useradd -r -g eucalyptus -d /var/lib/eucalyptus -s /sbin/nologin \
#    -c 'Eucalyptus' eucalyptus
getent passwd eucalyptus >/dev/null || \
    useradd -r -g eucalyptus -d /var/lib/eucalyptus \
    -c 'Eucalyptus' eucalyptus

if [ "$1" = "2" ]; then
    # Stop all old services
    if [ -x %{_initrddir}/eucalyptus-cloud ]; then
         /sbin/service eucalyptus-cloud stop
    fi
    if [ -x %{_initrddir}/eucalyptus-cc ]; then
         /sbin/service eucalyptus-cc cleanstop
    fi
    if [ -x %{_initrddir}/eucalyptus-nc ]; then
         /sbin/service eucalyptus-nc stop
    fi
    if [ -x %{_initrddir}/eucanetd ]; then
         /sbin/service eucanetd stop
    fi

    # Back up important data as well as all of the previous installation's jars.
    BACKUPDIR="/var/lib/eucalyptus/upgrade/eucalyptus.backup.`date +%%s`"
    mkdir -p "$BACKUPDIR"
    EUCABACKUPS=""
    for i in /var/lib/eucalyptus/keys/ /var/lib/eucalyptus/db/ /var/lib/eucalyptus/services /etc/eucalyptus/eucalyptus.conf /etc/eucalyptus/eucalyptus-version /usr/share/eucalyptus/; do
        if [ -e $i ]; then
            EUCABACKUPS="$EUCABACKUPS $i"
        fi
    done

    OLD_EUCA_VERSION=`cat /etc/eucalyptus/eucalyptus-version`
    echo "# This file was automatically generated by Eucalyptus packaging." > /etc/eucalyptus/.upgrade
    echo "$OLD_EUCA_VERSION:$BACKUPDIR" >> /etc/eucalyptus/.upgrade

    tar cf - $EUCABACKUPS 2>/dev/null | tar xf - -C "$BACKUPDIR" 2>/dev/null
fi
exit 0


%post blockdev-utils
# Reload udev rules
/sbin/service udev-post reload || :
exit 0


%post common-java
chkconfig --add eucalyptus-cloud
exit 0


%post sc
if [ -e %{_initrddir}/tgtd ]; then
    chkconfig --add tgtd
    /sbin/service tgtd start
fi
exit 0


%post cc
chkconfig --add eucalyptus-cc
exit 0


%post nc
if [ -e %{_initrddir}/libvirtd ]; then
    chkconfig --add libvirtd
    /sbin/service libvirtd restart
fi
chkconfig --add eucalyptus-nc
usermod -a -G kvm eucalyptus
exit 0


%post -n eucanetd
chkconfig --add eucanetd
exit 0


%postun blockdev-utils
# Reload udev rules on uninstall
if [ "$1" = "0" ]; then
    /sbin/service udev-post reload || :
fi
exit 0


%preun common-java
if [ "$1" = "0" ]; then
    if [ -f /etc/eucalyptus/eucalyptus.conf ]; then
        /sbin/service eucalyptus-cloud stop
    fi
    chkconfig --del eucalyptus-cloud
fi
exit 0


%preun cc
if [ "$1" = "0" ]; then
    if [ -f /etc/eucalyptus/eucalyptus.conf ]; then
        /sbin/service eucalyptus-cc cleanstop
    fi
    chkconfig --del eucalyptus-cc
fi
exit 0


%preun nc
if [ "$1" = "0" ]; then
    if [ -f /etc/eucalyptus/eucalyptus.conf ]; then
        /sbin/service eucalyptus-nc stop
    fi
    chkconfig --del eucalyptus-nc
fi
exit 0


%preun -n eucanetd
if [ "$1" = "0" ]; then
    if [ -f /etc/eucalyptus/eucalyptus.conf ]; then
        /sbin/service eucanetd stop
    fi
    chkconfig --del eucanetd
fi
exit 0


%changelog
* Mon Feb 29 2016 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.2.2
- Version bump (4.2.2)

* Tue Nov  3 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.2.1
- Version bump (4.2.1)

* Tue Sep 22 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.2.0
- Added /var/run/eucalyptus/net to eucanetd package (EUCA-11411)

* Mon Sep 21 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.2.0
- Pulled in python-requestbuilder >= 0.4 to fix unsigned redirects (EUCA-11378)

* Tue Sep  8 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.2.0
- Remove vmware admin tools

* Tue Jul 28 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.2.0
- Added pv dep to imaging-toolkit package

* Thu Jul 16 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.2.0
- Bumped python-requestbuilder dep to >= 0.3.2

* Mon Jun 29 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.2.0
- Added more new admin tools
- Added /etc/eucalyptus-admin

* Mon Jun 22 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.2.0
- Added ELB security policies (EUCA-10985)

* Tue Apr 14 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.1
- Added announce-arp support script for eucanetd (EUCA-10741)

* Thu Apr  9 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.2.0
- Version bump (4.2.0)

* Tue Apr  7 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.2.0
- Removed pre-4.0 Requires/Provides/Obsoletes
- Removed postgresql91 dependencies (only needed for 4.0 -> 4.1 upgrades)
- Removed pre-el6 leftovers
- Added first batch of new admin, support scripts

* Mon Mar 23 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.1
- Added libuuid-devel build dependency

* Mon Mar  9 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.1
- Dropped euca-install-service-image (EUCA-10369)

* Tue Jan 20 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0
- Made eucalyptus-cc depend on eucanetd for conntrack_kernel_params (EUCA-10405)

* Thu Jan 15 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0
- Added sample NC hooks as doc files (EUCA-9680)

* Tue Jan 13 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0
- Moved conntrack_kernel_params to eucanetd package (EUCA-10314)

* Mon Jan 12 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0
- Fixed typo in old db-home configure script option (EUCA-10319)

* Tue Jan  6 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0
- Reversed eucanetd -> eucalyptus-nc dependency (EUCA-10219)
- Removed unused font dependency
- Added postgresql91 bits for upgrades from 4.0.x (EUCA-10150)

* Fri Dec 19 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0
- Added euca-install-service-image to admin tools (EUCA-10201)
- Added service-images.yml for euca-install-service-image (EUCA-10202)
- Added PyYAML and euca2ools dependencies to support euca-install-service-image

* Tue Dec  2 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0
- Added /usr/share/eucalyptus/status

* Mon Nov  3 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0
- Added librados2 and librbd1 deps to sc and nc packages (EUCA-10099)
- Dropped drbd

* Wed Oct  8 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0
- Added nginx_proxy.conf to eucanetd package

* Fri Oct  3 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0
- Bumped nc's euca2ools dependency to >= 3.2
- Removed postgresql 9.1 dependencies (EUCA-9703)

* Fri Sep  5 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0
- Added eucalyptus-status group (EUCA-9958)
- Added /var/run/eucalyptus/status dir (EUCA-9958)

* Tue Sep  5 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.2
- Version bump (4.0.2)

* Tue Jul 22 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0-0
- Added build-time dependency on json-c-devel

* Thu Jun 19 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0-0
- Version bump (4.1.0)
- Added dependency on postgresql92 (EUCA-9700)

* Tue Jun 17 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.1-0
- Switched to monolithic source tarball naming

* Mon Jun 13 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.1-0
- Moved httpd-cc.conf and httpd-nc.conf to /var/run/eucalyptus
- Dropped osg package (EUCA-9468)
- Moved WS-Security client policies to /usr/share/eucalyptus/policies (EUCA-8706)

* Fri May 16 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.0-0
- Ensure openssl allows for credential download

* Thu May  8 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.0-0
- Dropped most new admin tool executables (EUCA-9064)

* Tue Apr 29 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.0-0
- Added euca-(de)register service and euca-describe-service-types

* Fri Apr  4 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.0-0
- Dropped unused validation stuff (EUCA-8569)
- Dropped old admin web UI stuff (EUCA-8616)

* Thu Feb 27 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.0-0
- Added euca-run-workflow

* Thu Feb 20 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.0-0
- Added new eucalyptus-imaging-toolkit subpackage
- Switched to stock dhcpd package (EUCA-6869)
- Renamed -eucanet subpackage to eucanetd (EUCA-8768)

* Fri Feb 14 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.0-0
- Add new admin tool executables

* Thu Nov 21 2013 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.0-0
- Update java requires and build requires for RHEL 6.5 support

* Tue Nov 19 2013 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.0-0
- Add get_bundle tool

* Mon Nov 11 2013 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.0-0
- Update to version 4.0.0

* Thu Oct 31 2013 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.4.1-0
- Add logrotate for CC/NC

* Thu Oct 17 2013 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.4.0-0
- nc sub-package now requires euca2ools 3.0.2 or later

* Fri Oct 04 2013 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.4.0-0
- Add eucalyptus-backup-restore

* Tue Sep 24 2013 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.4.0-0
- Added iptables-preload example to CC package

* Tue Sep 10 2013 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.4.0-0
- Remove console sub-package

* Wed Aug 28 2013 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.4.0-0
- Add eucanetd tech preview

* Wed Jul 17 2013 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.3.0-0
- Require postgresql >= 9.1.9

* Fri Jul  5 2013 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.4.0-0
- Added files for SAN common stuff

* Tue Jul  2 2013 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.4.0-0
- Dropped RHEL 5 support

* Mon Jun 21 2013 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.4.0-0
- Updated to 3.4.0

* Thu Jun 20 2013 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.3.1-0
- Version bump

* Thu Jun 20 2013 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.3.0.1-0
- Version bump

* Tue Mar 19 2013 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.3.0-0
- remove velocity Requires

* Fri Nov 30 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Added sample iscsid.conf docfile

* Tue Nov 27 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Added eucaconsole user and group
- Change ownership for console package files and directories
- Added /var/run/eucalyptus-console directory for writing pidfile

* Mon Nov 19 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Added sample multipath.conf docfile

* Wed Nov 13 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Reload udev rules in postun instead of preun

* Wed Oct 31 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- User Console python package changed from server => eucaconsole

* Fri Oct 26 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Updated eucadmin license tag

* Wed Oct 24 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Merged spec file content for Eucalyptus Console

* Tue Oct 16 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Added temporary fix for jasperreports jar removal
- Removed /etc/eucalyptus/cloud.d/reports directory

* Tue Oct 16 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Added iproute dependency to the cc package

* Mon Oct 15 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Added getstats_net.pl to the CC subpackage

* Wed Oct 10 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Moved DASManager to the sc package

* Mon Oct  8 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Added udev rules for drbd
- Reload udev rules on install and uninstall

* Sat Oct  6 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Added eureport-delete-data to files section

* Thu Oct  4 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Added device-mapper-multipath dependencies to sc and nc packages
- Added missing perl requires
- Added udev rules for multipath support

* Mon Sep 24 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Change ownership on /etc/eucalyptus to eucalyptus:eucalyptus
  This is a temporary fix for issue BROKER-9

* Fri Sep 21 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Updated reporting CLI tool names
- Added new perl dependencies for reporting

* Wed Sep 12 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Split java-common into java-common and java-common-libs

* Tue Sep  4 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Added report generation tool

* Thu Aug 23 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Added fault message dir

* Mon Jul 30 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.2.0-0
- Version bump

* Fri Jun  1 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1-0
- Moved 01_pg_kernel_params script to -cloud package

* Wed May 30 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1-0
- Dropped now-nonexistent volume management scripts

* Tue May 29 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1-0
- Treat eucalyptus.conf like a config file

* Fri May 25 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1-0
- Depend on bc so the eucalyptus-cloud init script works

* Wed Apr 23 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1-0
- Fixed bundled lib tarball explosion
- Swapped in configure --with-db-home
- Added extra version info
- Cleaned up extraneous build stuff

* Wed Apr 16 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1-0
- Dropped old udev reload

* Fri Apr 11 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1-0
- Depend on postgres, not mysql

* Mon Mar 19 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.0.1-2
- Added iSCSI client dependency to SC package

* Thu Mar 15 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.0.1-1
- Update to Eucalyptus 3.0.1 RC 1

* Wed Feb  8 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.0.0-3
- Update to Eucalyptus 3.0.0 RC 3

* Tue Feb  7 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.0.0-2
- Update to Eucalyptus 3.0.0 RC 2

* Thu Feb  2 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.0.0-1
- Update to Eucalyptus 3.0.0 RC 1

* Tue Jun  1 2010 Eucalyptus Release Engineering <support@eucalyptus.com> - 2.0.0-1
- Version 2.0 of Eucalyptus Enterprise Cloud
  - Windows VM Support
  - User/Group Management
  - SAN Integration
  - VMWare Hypervisor Support
