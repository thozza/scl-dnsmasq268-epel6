# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ruby193 in this case
%global scl dnsmasq268
%endif
%scl_package %scl

%global install_scl 1

Summary: Package that installs %scl
Name: %scl_name
Version: 1
Release: 1%{?dist}
License: GPLv2+
Requires: %{scl_prefix}dnsmasq
BuildRequires: scl-utils-build

%description
This is the main package for %scl Software Collection.
Provide some useful info about this SCL.

%package runtime
Summary: Package that handles %scl Software Collection
Requires: scl-utils
Requires: /usr/bin/scl_source

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Requires: scl-utils-build

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%prep
%setup -T -c

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_scl_scripts}/root
cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH=%{_bindir}\${PATH:+:\${PATH}}
export PATH=%{_sbindir}\${PATH:+:\${PATH}}
export LD_LIBRARY_PATH=%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
EOF
%scl_install
# generate a configuration file for daemon
cat >> %{buildroot}%{_scl_scripts}/service-environment << EOF
# Services are started in a fresh environment without any influence of user's
# environment (like environment variable values). As a consequence,
# information of all enabled collections will be lost during service start up.
# If user needs to run a service under any software collection enabled, this
# collection has to be written into DNSMASQ268_SCLS_ENABLED variable in
# /opt/rh/sclname/service-environment.
DNSMASQ268_SCLS_ENABLED="%{scl}"
EOF


%files

%files runtime
%scl_files
%config(noreplace) %{_scl_scripts}/service-environment

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%changelog
* Tue Mar 11 2014 Tomas Hozza <thozza@redhat.com> - 1-1
- Initial package.
