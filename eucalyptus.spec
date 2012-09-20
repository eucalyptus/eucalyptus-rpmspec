%if 0%{?el5}
%global euca_bridge       xenbr0
%global euca_build_req    vconfig, wget, rsync
%global euca_curl         curl
%global euca_dhcp         dhcp
%global euca_httpd        httpd
%global euca_hypervisor   xen
%global euca_iscsi_client iscsi-initiator-utils
%global euca_iscsi_server scsi-target-utils
%global euca_libcurl      curl-devel
%global euca_libvirt      libvirt >= 0.6
%global pybasever         26
%global __python_ver      2.6
%global __python          %{_bindir}/python%{__python_ver}
%global __os_install_post %{__multiple_python_os_install_post}
%endif
%if 0%{?fedora} || 0%{?rhel} >= 6
%global euca_bridge       br0
%global euca_build_req    vconfig, wget, rsync
%global euca_curl         curl
%global euca_httpd        httpd
%global euca_hypervisor   kvm
%global euca_iscsi_client iscsi-initiator-utils
%global euca_iscsi_server scsi-target-utils
%global euca_libcurl      curl-devel
%global euca_libvirt      libvirt
%endif
%if 0%{?rhel} >= 6
%global euca_dhcp         dhcp41
%endif
%if 0%{?fedora}
%global euca_dhcp         dhcp
%endif

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
Version:       3.1.2
Release:       0%{?build_id:.%build_id}%{?dist}
License:       GPLv3
URL:           http://www.eucalyptus.com
Group:         Applications/System

BuildRequires: ant >= 1.7
BuildRequires: ant-nodeps >= 1.7
BuildRequires: axis2-adb-codegen
BuildRequires: axis2-codegen
BuildRequires: axis2c-devel >= 1.6.0
BuildRequires: java-devel >= 1:1.6.0
BuildRequires: jpackage-utils
BuildRequires: libvirt-devel >= 0.6
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: openssl-devel
BuildRequires: python%{?pybasever}-devel
BuildRequires: python%{?pybasever}-setuptools
BuildRequires: rampartc-devel >= 1.3.0
BuildRequires: swig
BuildRequires: velocity
BuildRequires: xalan-j2-xsltc
BuildRequires: /usr/bin/awk

BuildRequires: %{euca_iscsi_client}
BuildRequires: %{euca_libvirt}-devel
BuildRequires: %{euca_libvirt}
BuildRequires: %{euca_libcurl}

Requires:      %{euca_build_req}
Requires:      libselinux-python
Requires:      perl(Crypt::OpenSSL::RSA)
Requires:      perl(Crypt::OpenSSL::Random)
Requires:      sudo
Requires:      /usr/bin/which
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd

%provide_abi

# Transition away from libraries in /opt
Obsoletes:     euca-axis2c   < 1.6.0-2
Obsoletes:     euca-rampartc < 1.3.0-7

BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Source0:       %{name}-%{version}%{?tar_suffix}.tar.gz
Source1:       cloud-lib.tar.gz
# A version of WSDL2C.sh that respects standard classpaths
Source2:       euca-WSDL2C.sh

# Eliminate the redundant "common" config section in drbd.conf
Patch1:        eucalyptus-3.0.0-drbd-common.patch

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
Requires:     jpackage-utils
Requires:     java >= 1:1.6.0
Requires:     lvm2
Requires:     velocity
Requires:     %{_sbindir}/euca_conf

%provide_abi common-java


%description common-java
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
Requires:     lvm2
Requires:     %{euca_iscsi_client}
Requires:     %{euca_iscsi_server}

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
Requires:     euca2ools >= 2.0
Requires:     lvm2
Requires:     perl(Getopt::Long)
%if 0%{?fedora}
Requires:     postgresql
Requires:     postgresql-server
%else
Requires:     postgresql91
Requires:     postgresql91-server
%endif

# For reporting web UI
%if 0%{?el5}
Requires:     bitstream-vera-fonts
%else
Requires:     dejavu-serif-fonts
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

%package cc
Summary:      Elastic Utility Computing Architecture - cluster controller
Group:        Applications/System

Requires:     %{name}    = %{version}-%{release}
Requires:     %{name}-gl = %{version}-%{release}
Requires:     bridge-utils
Requires:     iptables
Requires:     vtun
Requires:     %{euca_dhcp}
Requires:     %{euca_httpd}
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
Requires:     bridge-utils
Requires:     device-mapper
Requires:     euca2ools >= 2.0
# The next six come from storage/diskutil.c, which shells out to lots of stuff.
Requires:     coreutils
Requires:     e2fsprogs
Requires:     file
Requires:     parted
Requires:     util-linux
Requires:     %{euca_curl}
Requires:     %{euca_httpd}
Requires:     %{euca_hypervisor}
Requires:     %{euca_iscsi_client}
Requires:     %{euca_libvirt}
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
Requires:     %{euca_httpd}

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
Requires:     openssh-clients
Requires:     python%{?pybasever}-eucadmin = %{version}-%{release}
Requires:     rsync

%provide_abi admin-tools

%if ! 0%{?el5}
BuildArch:    noarch
%endif

%description admin-tools
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains command line tools necessary for managing a
Eucalyptus cluster.

%package -n python%{?pybasever}-eucadmin
Summary:      Elastic Utility Computing Architecture - administration Python library
License:      BSD
Group:        Development/Libraries

Requires:     python%{?pybasever}-boto >= 2.1
Requires:     rsync
%if 0%{?el5}
Requires:     postgresql91-python26
%else
Requires:     PyGreSQL
%endif

%provide_abi python%{?pybasever}-eucadmin

%if ! 0%{?el5}
BuildArch:    noarch
%endif

%description -n python%{?pybasever}-eucadmin
Eucalyptus is a service overlay that implements elastic computing
using existing resources. The goal of Eucalyptus is to allow sites
with existing clusters and server infrastructure to co-host an elastic
computing service that is interface-compatible with Amazon AWS.

This package contains the Python library used by Eucalyptus administration
tools.  It is neither intended nor supported for use by any other programs.

%prep
%setup -q -n %{name}-%{version}%{?tar_suffix}

%if 0%{?rhel} >= 6 || 0%{?fedora}
%patch1 -p1
%endif

%build
export CFLAGS="%{optflags}"

# Eucalyptus does not assign the usual meaning to prefix and other standard
# configure variables, so we can't realistically use %%configure.
./configure --with-axis2=%{_datadir}/axis2-* --with-axis2c=%{axis2c_home} --with-wsdl2c-sh=%{S:2} --enable-debug --prefix=/ --with-apache2-module-dir=%{_libdir}/httpd/modules --with-db-home=/usr/pgsql-9.1 --with-extra-version=%{release} --with-vddk=/opt/packages/vddk

# Untar the bundled cloud-lib Java dependencies.
mkdir clc/lib
tar xf %{S:1} -C clc/lib

# FIXME: storage/Makefile breaks with parallel make
make # %{?_smp_mflags}

%install
[ $RPM_BUILD_ROOT != "/" ] && rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

sed -i -e 's#.*EUCALYPTUS=.*#EUCALYPTUS="/"#' \
       -e 's#.*HYPERVISOR=.*#HYPERVISOR="%{euca_hypervisor}"#' \
       -e 's#.*INSTANCE_PATH=.*#INSTANCE_PATH="/var/lib/eucalyptus/instances"#' \
       -e 's#.*VNET_BRIDGE=.*#VNET_BRIDGE="%{euca_bridge}"#' \
       $RPM_BUILD_ROOT/etc/eucalyptus/eucalyptus.conf

# RHEL does not include support for SCSI emulation in KVM.
%if 0%{?rhel}
sed -i 's#.*USE_VIRTIO_DISK=.*#USE_VIRTIO_DISK="1"#' $RPM_BUILD_ROOT/etc/eucalyptus/eucalyptus.conf
sed -i 's#.*USE_VIRTIO_ROOT=.*#USE_VIRTIO_ROOT="1"#' $RPM_BUILD_ROOT/etc/eucalyptus/eucalyptus.conf
%endif

# Use patched dhcpd on el6
%if 0%{?el6}
sed -i 's#.*VNET_DHCPDAEMON=.*#VNET_DHCPDAEMON="/usr/sbin/dhcpd41"#' $RPM_BUILD_ROOT/etc/eucalyptus/eucalyptus.conf
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
%if 0%{?fedora} || 0%{?rhel} >= 6
mkdir -p $RPM_BUILD_ROOT/var/lib/polkit-1/localauthority/10-vendor.d
cp -p tools/eucalyptus-nc-libvirt.pkla $RPM_BUILD_ROOT/var/lib/polkit-1/localauthority/10-vendor.d/eucalyptus-nc-libvirt.pkla
%endif

# Work around a regression in libvirtd.conf file handling that appears
# in at least RHEL 6.2
# https://www.redhat.com/archives/libvirt-users/2011-July/msg00039.html
mkdir $RPM_BUILD_ROOT/var/lib/eucalyptus/.libvirt
touch $RPM_BUILD_ROOT/var/lib/eucalyptus/.libvirt/libvirtd.conf

# Install the NC hook that attempts to restart failed libvirtd on systems that
# need it
# https://eucalyptus.atlassian.net/browse/EUCA-3421
%if 0%{?rhel}
cp -p tools/nc-hooks/libvirt-check.sh $RPM_BUILD_ROOT/etc/eucalyptus/nc-hooks/libvirt-check.sh
%endif

%clean
[ $RPM_BUILD_ROOT != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE INSTALL README CHANGELOG

%dir /etc/eucalyptus
%config(noreplace) /etc/eucalyptus/eucalyptus.conf
/etc/eucalyptus/eucalyptus-version
/etc/eucalyptus/httpd.conf
%ghost /etc/eucalyptus/httpd-tmp.conf

%attr(-,root,eucalyptus) %dir /usr/lib/eucalyptus
%attr(4750,root,eucalyptus) /usr/lib/eucalyptus/euca_mountwrap
%attr(4750,root,eucalyptus) /usr/lib/eucalyptus/euca_rootwrap

/usr/sbin/euca_sync_key

%dir /usr/share/eucalyptus
/usr/share/eucalyptus/add_key.pl
/usr/share/eucalyptus/connect_iscsitarget.pl
/usr/share/eucalyptus/create-loop-devices
/usr/share/eucalyptus/disconnect_iscsitarget.pl
%doc /usr/share/eucalyptus/doc/
/usr/share/eucalyptus/euca_ipt
/usr/share/eucalyptus/euca_upgrade
/usr/share/eucalyptus/floppy
/usr/share/eucalyptus/get_iscsitarget.pl
/usr/share/eucalyptus/populate_arp.pl
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/db
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/keys
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/upgrade
# Can this file go into a single-component package?  What uses it?
/var/lib/eucalyptus/keys/cc-client-policy.xml
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
/etc/eucalyptus/cloud.d/reports/
/etc/eucalyptus/cloud.d/scripts/
/etc/eucalyptus/cloud.d/security.policy
/etc/eucalyptus/cloud.d/upgrade/
/etc/eucalyptus/cloud.d/www/
/usr/sbin/eucalyptus-cloud
/usr/share/eucalyptus/*jar*
%doc /usr/share/eucalyptus/licenses/
%ghost /var/lib/eucalyptus/services
%attr(-,eucalyptus,eucalyptus) /var/lib/eucalyptus/webapps/

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
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/volumes
/usr/share/eucalyptus/connect_iscsitarget_sc.pl
/usr/share/eucalyptus/disconnect_iscsitarget_sc.pl
/usr/lib/eucalyptus/liblvm2control.so

%files cc
%defattr(-,root,root,-)
%{_initrddir}/eucalyptus-cc
%{axis2c_home}/services/EucalyptusCC/
%attr(-,eucalyptus,eucalyptus) %dir /var/lib/eucalyptus/CC
%ghost /etc/eucalyptus/httpd-cc.conf
/etc/eucalyptus/vtunall.conf.template
/usr/lib/eucalyptus/shutdownCC
/usr/share/eucalyptus/dynserv.pl
# Is this used?
/var/lib/eucalyptus/keys/nc-client-policy.xml

%files nc
%defattr(-,root,root,-)
%config(noreplace) /etc/eucalyptus/libvirt.xsl
%dir /etc/eucalyptus/nc-hooks
/etc/eucalyptus/nc-hooks/example.sh
%if 0%{?rhel}
/etc/eucalyptus/nc-hooks/libvirt-check.sh
%endif
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
%if 0%{?fedora} || 0%{?rhel} >= 6
/var/lib/polkit-1/localauthority/10-vendor.d/eucalyptus-nc-libvirt.pkla
%endif

%files gl
%defattr(-,root,root,-)
%{axis2c_home}/services/EucalyptusGL/

%files admin-tools
%defattr(-,root,root,-)
%{_sbindir}/euca_conf
%{_sbindir}/euca-configure-vmware
%{_sbindir}/euca-deregister-arbitrator
%{_sbindir}/euca-deregister-cloud
%{_sbindir}/euca-deregister-cluster
%{_sbindir}/euca-deregister-storage-controller
%{_sbindir}/euca-deregister-vmware-broker
%{_sbindir}/euca-deregister-walrus
%{_sbindir}/euca-describe-arbitrators
%{_sbindir}/euca-describe-clouds
%{_sbindir}/euca-describe-clusters
%{_sbindir}/euca-describe-components
%{_sbindir}/euca-describe-nodes
%{_sbindir}/euca-describe-properties
%{_sbindir}/euca-describe-services
%{_sbindir}/euca-describe-storage-controllers
%{_sbindir}/euca-describe-vmware-brokers
%{_sbindir}/euca-describe-walruses
%{_sbindir}/euca-get-credentials
%{_sbindir}/euca-modify-cluster
%{_sbindir}/euca-modify-property
%{_sbindir}/euca-modify-service
%{_sbindir}/euca-modify-storage-controller
%{_sbindir}/euca-modify-walrus
%{_sbindir}/euca-register-arbitrator
%{_sbindir}/euca-register-cloud
%{_sbindir}/euca-register-cluster
%{_sbindir}/euca-register-storage-controller
%{_sbindir}/euca-register-vmware-broker
%{_sbindir}/euca-register-walrus

%files -n python%{?pybasever}-eucadmin
%defattr(-,root,root,-)
%{python_sitelib}/eucadmin*

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

    # Back up important data as well as all of the previous installation's jars.
    BACKUPDIR="/var/lib/eucalyptus/upgrade/eucalyptus.backup.`date +%%s`"
    ## FIXME:  What cleans this file up?
    echo "$BACKUPDIR" > /tmp/eucaback.dir
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
if [ "$1" = "2" ]; then
    if [ -f /tmp/eucaback.dir ]; then
        BACKDIR=`cat /tmp/eucaback.dir`
        if [ -d "$BACKDIR" ]; then
            /usr/share/eucalyptus/euca_upgrade --old $BACKDIR --new / --conf >/var/log/eucalyptus/upgrade-config.log 2>&1
        fi
    fi
fi

# Clean up after old releases that didn't enumerate all admin-tools files
rm -rf /usr/sbin/euca_admin

exit 0

%post common-java
chkconfig --add eucalyptus-cloud

%post cloud
%if 0%{?el5}
if [ -e /etc/sysconfig/system-config-securitylevel ]; then
    if ! grep -q 8773:tcp /etc/sysconfig/system-config-securitylevel; then
        echo "--port=8773:tcp" >> /etc/sysconfig/system-config-securitylevel
        echo "--port=8443:tcp" >> /etc/sysconfig/system-config-securitylevel
    fi
fi
%endif
exit 0

%post sc
if [ -e %{_initrddir}/tgtd ]; then
    chkconfig --add tgtd
    /sbin/service tgtd start
fi
exit 0

%post cc
chkconfig --add eucalyptus-cc
%if 0%{?el5}
if [ -e /etc/sysconfig/system-config-securitylevel ]; then
    if ! grep -q 8774:tcp /etc/sysconfig/system-config-securitylevel; then
        echo "--port=8774:tcp" >> /etc/sysconfig/system-config-securitylevel
    fi
fi
%endif
exit 0

%post nc
if [ -e %{_initrddir}/libvirtd ]; then
    chkconfig --add libvirtd
    /sbin/service libvirtd restart
fi
chkconfig --add eucalyptus-nc
%if 0%{?fedora} || 0%{?rhel} >= 6
    usermod -a -G kvm eucalyptus
%endif
%if 0%{?el5}
    if [ -e /etc/sysconfig/system-config-securitylevel ]; then
        if ! grep -q 8775:tcp /etc/sysconfig/system-config-securitylevel; then
        echo "--port=8775:tcp" >> /etc/sysconfig/system-config-securitylevel
    fi
fi
%endif
exit 0

%if 0%{?el5}
%preun cloud
if [ "$1" = "0" ]; then
    if [ -e /etc/sysconfig/system-config-securitylevel ]; then
        sed -e '/^--port=8773/ d' -e '/^--port=8443/ d' -i /etc/sysconfig/system-config-securitylevel
    fi
fi
exit 0
%endif

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
%if 0%{?el5}
    if [ -e /etc/sysconfig/system-config-securitylevel ]; then
        sed -i '/^--port=8774/ d' /etc/sysconfig/system-config-securitylevel
    fi
%endif
fi
exit 0

%preun nc
if [ "$1" = "0" ]; then
    if [ -f /etc/eucalyptus/eucalyptus.conf ]; then
        /sbin/service eucalyptus-nc stop
    fi
    chkconfig --del eucalyptus-nc
%if 0%{?el5}
    if [ -e /etc/sysconfig/system-config-securitylevel ]; then
        sed -i '/^--port=8775/ d' /etc/sysconfig/system-config-securitylevel
    fi
%endif
fi
exit 0

%changelog
* Thu Sep 20 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.2-0
- Added openssh-clients dependency to admin-tools package

* Thu Sep  6 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.2-0
- Version bump
- Added libvirt-check NC hook [EUCA-3421]

* Fri Jul 20 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 3.1.1-0
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
