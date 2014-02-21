%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define provide_abi() \
%{!?abi_version: %define abi_version %{version}-%{release}} \
%if 0%# \
Provides: %{name}-abi(%1) = %{abi_version} \
%else \
Provides: %{name}-abi = %{abi_version} \
%endif \
%{nil}

Summary:       Elastic Utility Computing Architecture
Name:          eucalyptus
Version:       4.0.0
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

Requires:      libselinux-python
Requires:      perl(Crypt::OpenSSL::RSA)
Requires:      perl(Crypt::OpenSSL::Random)
Requires:      rsync
Requires:      sudo
Requires:      vconfig
Requires:      wget
Requires:      /usr/bin/which
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd

%provide_abi

BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Source0:       %{name}-%{version}%{?tar_suffix}.tar.gz
Source1:       cloud-lib.tar.gz
# A version of WSDL2C.sh that respects standard classpaths
Source2:       euca-WSDL2C.sh

# Eliminate the redundant "common" config section in drbd.conf
Patch1:        eucalyptus-3.4.0-drbd-common.patch

%description
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the common parts; you will need to install at
least one of the cloud controller (cloud), cluster controller (cc),
node controller (nc), storage controller (sc), or walrus packages as well.


%package common-java
Summary:      Elastic Utility Computing Architecture - ws java stack
Group:        Applications/System
Requires:     %{name} = %{version}-%{release}
Requires:     %{name}-common-java-libs = %{version}-%{release}
Requires:     lvm2
Requires:     %{_sbindir}/euca_conf

%provide_abi common-java

%description common-java
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the common-java files.


%package common-java-libs
Summary:      Elastic Utility Computing Architecture - ws java stack libs
Group:        Applications/System

Requires:     jpackage-utils
Requires:     java-1.7.0-openjdk >= 1:1.7.0

Obsoletes:    eucalyptus-enterprise-storage-san-common-libs < 3.4.0
Provides:     eucalyptus-enterprise-storage-san-common-libs = %{version}-%{release}

%provide_abi common-java-libs

%description common-java-libs
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the java WS stack.


%package walrus
Summary:      Elastic Utility Computing Architecture - walrus
Group:        Applications/System

Requires:     %{name}             = %{version}-%{release}
Requires:     %{name}-common-java = %{version}-%{release}
%if 0%{?rhel}
# CentOS Extras and ELRepo have differing package names, but compatible Provides
#
# Watch out for yum pulling in modules for the wrong kernel on systems that run
# kernel-xen, kernel-PAE, etc.
Requires:     drbd83
Requires:     drbd83-kmod
%endif
%if 0%{?fedora}
Requires:     drbd-utils
%endif
Requires:     lvm2

%provide_abi walrus

%description walrus
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains storage component for your cloud: images and buckets
are handled by walrus. Typically this package is installed alongside the
cloud controller.


%package sc
Summary:      Elastic Utility Computing Architecture - storage controller
Group:        Applications/System

Requires:     %{name}             = %{version}-%{release}
Requires:     %{name}-common-java = %{version}-%{release}
Requires:     device-mapper-multipath
Requires:     iscsi-initiator-utils
Requires:     lvm2
Requires:     scsi-target-utils

Obsoletes:    eucalyptus-enterprise-storage-san-common < 3.4.0
Provides:     eucalyptus-enterprise-storage-san-common = %{version}-%{release}

%provide_abi sc

%description sc
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the storage controller part of eucalyptus, which
handles the elastic blocks for a given cluster. Typically you install it
alongside the cluster controller.


%package cloud
Summary:      Elastic Utility Computing Architecture - cloud controller
Group:        Applications/System

Requires:     %{name}                     = %{version}-%{release}
Requires:     %{name}-common-java%{?_isa} = %{version}-%{release}
# bc is needed for /etc/eucalyptus/cloud.d/init.d/01_pg_kernel_params
Requires:     bc
# For reporting web UI
Requires:     dejavu-serif-fonts
Requires:     euca2ools >= 2.0
Requires:     lvm2
Requires:     perl(Getopt::Long)
%if 0%{?fedora}
Requires:     postgresql >= 9.1.9
Requires:     postgresql-server >= 9.1.9
%else
Requires:     postgresql91 >= 9.1.9
Requires:     postgresql91-server >= 9.1.9
%endif

%provide_abi cloud

%description cloud
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the cloud controller part of eucalyptus. The cloud
controller needs to be reachable by both the cluster controller and from
the cloud clients.


%package osg
Summary:      Elastic Utility Computing Architecture - object storage gateway
Group:        Applications/System

Requires:     %{name}                          = %{version}-%{release}
Requires:     %{name}-common-java-libs%{?_isa} = %{version}-%{release}

%provide_abi osg

%description osg
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the object storage gateway of eucalyptus.


%package cc
Summary:      Elastic Utility Computing Architecture - cluster controller
Group:        Applications/System

Requires:     %{name}    = %{version}-%{release}
Requires:     %{name}-gl = %{version}-%{release}
Requires:     bridge-utils
Requires:     dhcp >= 4.1.1-33.P1
Requires:     httpd
Requires:     iproute
Requires:     iptables
Requires:     iputils
Requires:     vtun
Requires:     %{_sbindir}/euca_conf

%provide_abi cc

%description cc
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the cluster controller part of eucalyptus. It
handles a group of node controllers.


%package nc
Summary:      Elastic Utility Computing Architecture - node controller
Group:        Applications/System

Requires:     %{name}    = %{version}-%{release}
Requires:     %{name}-gl = %{version}-%{release}
Requires:     %{name}-imaging-toolkit = %{version}-%{release}
Requires:     bridge-utils
Requires:     device-mapper
Requires:     device-mapper-multipath
Requires:     euca2ools >= 3.0.2
Requires:     httpd
Requires:     iscsi-initiator-utils
Requires:     kvm
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
Requires:     util-linux
Requires:     %{_sbindir}/euca_conf

%provide_abi nc

%description nc
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the node controller part of eucalyptus. This
component handles instances.


%package gl
Summary:      Elastic Utility Computing Architecture - log service
Group:        Applications/System

Requires:     %{name} = %{version}-%{release}
Requires:     httpd

%provide_abi gl

%description gl
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the internal log service of eucalyptus.


%package admin-tools
Summary:      Elastic Utility Computing Architecture - admin CLI tools
License:      BSD
Group:        Applications/System

Requires:     %{name} = %{version}-%{release}
Requires:     python-eucadmin = %{version}-%{release}
Requires:     rsync

BuildArch:    noarch

%provide_abi admin-tools

%description admin-tools
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains command line tools necessary for managing a
Eucalyptus cluster.


%package -n python-eucadmin
Summary:      Elastic Utility Computing Architecture - administration Python library
# A patched version of python's gzip is included, so we add the Python license
License:      BSD and Python
Group:        Development/Libraries

Requires:     PyGreSQL
Requires:     python-boto >= 2.1
Requires:     rsync
Requires:     m2crypto

BuildArch:    noarch

%provide_abi python-eucadmin

%description -n python-eucadmin
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the Python library used by Eucalyptus administration
tools.  It is neither intended nor supported for use by any other programs.


%package -n eucanetd
Summary:        Elastic Utility Computing Architecture - edge networking daemon
License:        GPLv3
Group:          Applications/System

Requires:       %{name}-nc = %{version}-%{release}
Requires:       dhcp >= 4.1.1-33.P1
Requires:       ebtables
Requires:       ipset
Requires:       iptables

%provide_abi eucanetd

Obsoletes:      eucalyptus-eucanet < 4.0

%description -n eucanetd
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the daemon that controls the edge networking mode.
To use edge networking mode, all node controllers must have this package
installed.


%package imaging-toolkit
Summary:      Elastic Utility Computing Architecture - image manipulation tookit
License:      ASL 2.0

# This includes both things under tools/imaging and storage.
## FIXME:  euca2ools should require version >= 3.1
Requires:     euca2ools >= 3.0
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

%provide_abi imaging-toolkit

%description
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains a toolkit used internally by Eucalyptus to download and upload virtual machine images and to convert them between formats.


%prep
%setup -q -n %{name}-%{version}%{?tar_suffix}
%patch1 -p1

# Filter unwanted perl provides
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
sed -e '/perl(disconnect_iscsitarget_main.pl)/d' \
    -e '/perl(connect_iscsitarget_main.pl)/d' \
    -e '/perl(iscsitarget_common.pl)/d'
EOF

%global __perl_provides %{_builddir}/%{name}-%{version}%{?tar_suffix}/%{name}-prov
chmod +x %{__perl_provides}


# Filter unwanted perl requires
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
sed -e '/perl(disconnect_iscsitarget_main.pl)/d' \
    -e '/perl(connect_iscsitarget_main.pl)/d' \
    -e '/perl(iscsitarget_common.pl)/d'
EOF

%global __perl_requires %{_builddir}/%{name}-%{version}%{?tar_suffix}/%{name}-req
chmod +x %{__perl_requires}


%build
export CFLAGS="%{optflags}"

# Eucalyptus does not assign the usual meaning to prefix and other standard
# configure variables, so we can't realistically use %%configure.
./configure --with-axis2=%{_datadir}/axis2-* --with-axis2c=%{axis2c_home} --with-wsdl2c-sh=%{S:2} --enable-debug --prefix=/ --with-apache2-module-dir=%{_libdir}/httpd/modules --with-db-home=/usr/pgsql-9.1 --with-extra-version=%{release} --with-vddk=/opt/packages/vddk

# Untar the bundled cloud-lib Java dependencies.
mkdir clc/lib
tar xf %{S:1} -C clc/lib

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

# RHEL does not include support for SCSI emulation in KVM.
%if 0%{?rhel}
sed -i 's#.*USE_VIRTIO_DISK=.*#USE_VIRTIO_DISK="1"#' $RPM_BUILD_ROOT/etc/eucalyptus/eucalyptus.conf
sed -i 's#.*USE_VIRTIO_ROOT=.*#USE_VIRTIO_ROOT="1"#' $RPM_BUILD_ROOT/etc/eucalyptus/eucalyptus.conf
sed -i 's#.*USE_VIRTIO_NET=.*#USE_VIRTIO_NET="1"#' $RPM_BUILD_ROOT/etc/eucalyptus/eucalyptus.conf
%endif

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

# Touch httpd config files that the init scripts create so we can %ghost them
touch $RPM_BUILD_ROOT/etc/eucalyptus/httpd-{cc,nc,tmp}.conf

# Add PolicyKit config on systems that support it
mkdir -p $RPM_BUILD_ROOT/var/lib/polkit-1/localauthority/10-vendor.d
cp -p tools/eucalyptus-nc-libvirt.pkla $RPM_BUILD_ROOT/var/lib/polkit-1/localauthority/10-vendor.d/eucalyptus-nc-libvirt.pkla

# Put udev rules in the right place
mkdir -p $RPM_BUILD_ROOT/etc/udev/rules.d
cp -p $RPM_BUILD_ROOT/usr/share/eucalyptus/udev/rules.d/12-dm-permissions.rules $RPM_BUILD_ROOT/etc/udev/rules.d/12-dm-permissions.rules
cp -p $RPM_BUILD_ROOT/usr/share/eucalyptus/udev/rules.d/55-openiscsi.rules $RPM_BUILD_ROOT/etc/udev/rules.d/55-openiscsi.rules
cp -p $RPM_BUILD_ROOT/usr/share/eucalyptus/udev/rules.d/65-drbd-owner.rules $RPM_BUILD_ROOT/etc/udev/rules.d/65-drbd-owner.rules
# FIXME:  iscsidev.sh belongs in /usr/share/eucalyptus [RT:2093]
mkdir -p $RPM_BUILD_ROOT/etc/udev/scripts
install -m 0755 $RPM_BUILD_ROOT/usr/share/eucalyptus/udev/iscsidev.sh $RPM_BUILD_ROOT/etc/udev/scripts/iscsidev.sh
rm -rf $RPM_BUILD_ROOT/usr/share/eucalyptus/udev

# Work around a regression in libvirtd.conf file handling that appears
# in at least RHEL 6.2
# https://www.redhat.com/archives/libvirt-users/2011-July/msg00039.html
mkdir $RPM_BUILD_ROOT/var/lib/eucalyptus/.libvirt
touch $RPM_BUILD_ROOT/var/lib/eucalyptus/.libvirt/libvirtd.conf

# Remove README file if one exists
rm -f $RPM_BUILD_ROOT/usr/share/eucalyptus/README


%clean
[ $RPM_BUILD_ROOT != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE INSTALL README
%doc tools/multipath.conf.example.* tools/iscsid.conf.example

%attr(-,eucalyptus,eucalyptus) %dir /etc/eucalyptus
%config(noreplace) /etc/eucalyptus/eucalyptus.conf
/etc/eucalyptus/eucalyptus-version
/etc/eucalyptus/httpd.conf
%ghost /etc/eucalyptus/httpd-tmp.conf
# Needed for multipath on NCs and SAN-enabled SCs
/etc/udev/rules.d/12-dm-permissions.rules
/etc/udev/rules.d/65-drbd-owner.rules

%attr(-,root,eucalyptus) %dir /usr/lib/eucalyptus
%attr(4750,root,eucalyptus) /usr/lib/eucalyptus/euca_mountwrap
%attr(4750,root,eucalyptus) /usr/lib/eucalyptus/euca_rootwrap

# Kernel parameters required to be set for CC and NC
%attr(-,root,eucalyptus) %dir /usr/libexec/eucalyptus
%attr(0755,root,eucalyptus) /usr/libexec/eucalyptus/conntrack_kernel_params

# Common logrotate configuration for CC and NC
/etc/logrotate.d/eucalyptus

/usr/sbin/euca_sync_key
/usr/sbin/euca-generate-fault

%dir /usr/share/eucalyptus
/usr/share/eucalyptus/add_key.pl
/usr/share/eucalyptus/connect_iscsitarget.pl
/usr/share/eucalyptus/connect_iscsitarget_main.pl
/usr/share/eucalyptus/create-loop-devices
/usr/share/eucalyptus/disconnect_iscsitarget.pl
/usr/share/eucalyptus/disconnect_iscsitarget_main.pl
/usr/share/eucalyptus/generate-migration-keys.sh
/usr/share/eucalyptus/authorize-migration-keys.pl
%doc /usr/share/eucalyptus/doc/
/usr/share/eucalyptus/euca_ipt
/usr/share/eucalyptus/euca_upgrade
/usr/share/eucalyptus/faults/
/usr/share/eucalyptus/floppy
/usr/share/eucalyptus/get_iscsitarget.pl
/usr/share/eucalyptus/iscsitarget_common.pl
/usr/share/eucalyptus/populate_arp.pl
/usr/share/eucalyptus/get_bundle
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/db
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/keys
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/upgrade
# Can this file go into a single-component package?  What uses it?
/var/lib/eucalyptus/keys/cc-client-policy.xml
/var/lib/eucalyptus/keys/sc-client-policy.xml
%attr(-,eucalyptus,eucalyptus) %dir /var/log/eucalyptus
%attr(-,eucalyptus,eucalyptus) %dir /var/run/eucalyptus


%files common-java
%defattr(-,root,root,-)
%{_initrddir}/eucalyptus-cloud
# cloud.d contains random stuff used by every Java component.  Most of it
# probably belongs in /usr/share, but moving it will be painful.
%dir /etc/eucalyptus/cloud.d
/etc/eucalyptus/cloud.d/conf/
/etc/eucalyptus/cloud.d/drbd/
/etc/eucalyptus/cloud.d/eucalyptus-web-default.properties
/etc/eucalyptus/cloud.d/eucalyptus-web.properties
/etc/eucalyptus/cloud.d/gwt-web.xml
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
/usr/share/eucalyptus/lic_default
/usr/share/eucalyptus/lic_template


%files walrus
%defattr(-,root,root,-)
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/bukkits
/etc/eucalyptus/drbd.conf.example


%files sc
%defattr(-,root,root,-)
/etc/udev/rules.d/55-openiscsi*.rules
/etc/udev/scripts/iscsidev.sh
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/volumes
/usr/share/eucalyptus/connect_iscsitarget_sc.pl
/usr/share/eucalyptus/disconnect_iscsitarget_sc.pl


%files osg
# No files


%files cc
%defattr(-,root,root,-)
%{_initrddir}/eucalyptus-cc
%{axis2c_home}/services/EucalyptusCC/
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/CC
%ghost /etc/eucalyptus/httpd-cc.conf
/usr/share/eucalyptus/vtunall.conf.template
/usr/lib/eucalyptus/shutdownCC
/usr/share/eucalyptus/dynserv.pl
/usr/share/eucalyptus/getstats_net.pl
# Is this used?
/var/lib/eucalyptus/keys/nc-client-policy.xml


%files nc
%defattr(-,root,root,-)
%config(noreplace) /etc/eucalyptus/libvirt.xsl
%dir /etc/eucalyptus/nc-hooks
/etc/eucalyptus/nc-hooks/example.sh
%{_initrddir}/eucalyptus-nc
%{axis2c_home}/services/EucalyptusNC/
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/instances
%ghost /etc/eucalyptus/httpd-nc.conf
/usr/sbin/euca_test_nc
/usr/share/eucalyptus/detach.pl
/usr/share/eucalyptus/gen_kvm_libvirt_xml
/usr/share/eucalyptus/gen_libvirt_xml
/usr/share/eucalyptus/getstats.pl
/usr/share/eucalyptus/get_sys_info
/usr/share/eucalyptus/get_xen_info
/usr/share/eucalyptus/partition2disk
%attr(-,eucalyptus,eucalyptus) /var/lib/eucalyptus/.libvirt/
/var/lib/polkit-1/localauthority/10-vendor.d/eucalyptus-nc-libvirt.pkla


%files gl
%defattr(-,root,root,-)
%{axis2c_home}/services/EucalyptusGL/


%files admin-tools
%defattr(-,root,root,-)
%{_sbindir}/euca_conf
%{_sbindir}/euca-configure-vmware
%{_sbindir}/euca-deregister-arbitrator
%{_sbindir}/euca-deregister-autoscaling
%{_sbindir}/euca-deregister-cloud
%{_sbindir}/euca-deregister-cloudformation
%{_sbindir}/euca-deregister-cloudwatch
%{_sbindir}/euca-deregister-cluster
%{_sbindir}/euca-deregister-compute
%{_sbindir}/euca-deregister-euare
%{_sbindir}/euca-deregister-loadbalancing
%{_sbindir}/euca-deregister-object-storage-gateway
%{_sbindir}/euca-deregister-storage-controller
%{_sbindir}/euca-deregister-tokens
%{_sbindir}/euca-deregister-vmware-broker
%{_sbindir}/euca-deregister-walrus
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
%{_sbindir}/euca-describe-storage-controllers
%{_sbindir}/euca-describe-tokens
%{_sbindir}/euca-describe-vmware-brokers
%{_sbindir}/euca-describe-walruses
%{_sbindir}/euca-get-credentials
%{_sbindir}/euca-migrate-instances
%{_sbindir}/euca-modify-cluster
%{_sbindir}/euca-modify-property
%{_sbindir}/euca-modify-service
%{_sbindir}/euca-modify-storage-controller
%{_sbindir}/euca-modify-walrus
%{_sbindir}/euca-register-arbitrator
%{_sbindir}/euca-register-autoscaling
%{_sbindir}/euca-register-cloud
%{_sbindir}/euca-register-cloudformation
%{_sbindir}/euca-register-cloudwatch
%{_sbindir}/euca-register-cluster
%{_sbindir}/euca-register-compute
%{_sbindir}/euca-register-euare
%{_sbindir}/euca-register-loadbalancing
%{_sbindir}/euca-register-object-storage-gateway
%{_sbindir}/euca-register-storage-controller
%{_sbindir}/euca-register-tokens
%{_sbindir}/euca-register-user-services
%{_sbindir}/euca-register-vmware-broker
%{_sbindir}/euca-register-walrus
%{_sbindir}/euca-validator
%{_sbindir}/eureport-generate-report
%{_sbindir}/eureport-export-data
%{_sbindir}/eureport-delete-data


%files -n python-eucadmin
%defattr(-,root,root,-)
%{python_sitelib}/eucadmin*
/usr/lib/eucadmin/


%files -n eucanetd
%defattr(-,root,root,-)
%{_sbindir}/eucanetd
%{_initrddir}/eucanetd


%files imaging-toolkit
# TODO:  something should own %{_libexecdir}/eucalyptus
%{_libexecdir}/eucalyptus/euca-imager
%{python_sitelib}/eucatoolkit*


%pre
getent group eucalyptus >/dev/null || groupadd -r eucalyptus
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


%post
# Reload udev rules
/sbin/service udev-post reload || :
exit 0


%post common-java
chkconfig --add eucalyptus-cloud


%post sc
if [ -e %{_initrddir}/tgtd ]; then
    chkconfig --add tgtd
    /sbin/service tgtd start
fi
exit 0


%post cc
chkconfig --add eucalyptus-cc

if [ $1 -eq 2 -a ! -e /etc/eucalyptus/iptables-preload -a -f /var/run/eucalyptus/iptables-preload ]; then
    # Migrate /var/run/eucalyptus/iptables-preload (EUCA-3693, for eucalyptus 3.2.1)
    mv /var/run/eucalyptus/iptables-preload /etc/eucalyptus/iptables-preload
fi
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


%postun
# Reload udev rules on uninstall
if [ "$1" = "0" ]; then
    /sbin/service udev-post reload || :
fi


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
