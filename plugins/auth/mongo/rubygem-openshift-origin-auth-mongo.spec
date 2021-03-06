%if 0%{?fedora}%{?rhel} <= 6
    %global scl ruby193
    %global scl_prefix ruby193-
%endif
%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}
%global gem_name openshift-origin-auth-mongo
%global rubyabi 1.9.1

Summary:       OpenShift plugin for mongo auth service
Name:          rubygem-%{gem_name}
Version:       1.1.3
Release:       1%{?dist}
Group:         Development/Languages
License:       ASL 2.0
URL:           http://openshift.redhat.com
Source0:       http://mirror.openshift.com/pub/openshift-origin/source/%{gem_name}/rubygem-%{gem_name}-%{version}.tar.gz
Requires:      %{?scl:%scl_prefix}ruby(abi) = %{rubyabi}
Requires:      %{?scl:%scl_prefix}ruby
Requires:      %{?scl:%scl_prefix}rubygems
Requires:      %{?scl:%scl_prefix}rubygem(activeresource)
Requires:      %{?scl:%scl_prefix}rubygem(json)
Requires:      %{?scl:%scl_prefix}rubygem(mocha)
Requires:      rubygem(openshift-origin-common)
Requires:      openshift-origin-broker
Requires:      selinux-policy-targeted
Requires:      policycoreutils-python
Requires:      openssl
%if 0%{?fedora}%{?rhel} <= 6
BuildRequires: ruby193-build
BuildRequires: scl-utils-build
%endif
BuildRequires: %{?scl:%scl_prefix}ruby(abi) = %{rubyabi}
BuildRequires: %{?scl:%scl_prefix}ruby 
BuildRequires: %{?scl:%scl_prefix}rubygems
BuildRequires: %{?scl:%scl_prefix}rubygems-devel
BuildArch:     noarch
Provides:      rubygem(%{gem_name}) = %version
Obsoletes:     rubygem-swingshift-mongo-plugin

%description
Provides a mongo auth service based plugin

%package doc
Summary:        OpenShift plugin for mongo auth service ri documentation

%description doc
OpenShift plugin for mongo auth service ri documentation

%prep
%setup -q

%build
%{?scl:scl enable %scl - << \EOF}
mkdir -p .%{gem_dir}
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
# gem install compiles any C extensions and installs into a directory
# We set that to be a local directory so that we can move it into the
# buildroot in %%install
gem install -V \
        --local \
        --install-dir .%{gem_dir} \
        --bindir ./%{_bindir} \
        --force \
        --rdoc \
        %{gem_name}-%{version}.gem
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

# If there were programs installed:
mkdir -p %{buildroot}/usr/bin
cp -a ./%{_bindir}/* %{buildroot}/usr/bin

mkdir -p %{buildroot}/etc/openshift/plugins.d
cp %{buildroot}/%{gem_instdir}/conf/openshift-origin-auth-mongo.conf.example %{buildroot}/etc/openshift/plugins.d/


%files
%doc LICENSE COPYRIGHT Gemfile
%exclude %{gem_cache}
%{gem_instdir}
%{gem_spec}
/usr/bin/*
/etc/openshift/plugins.d/openshift-origin-auth-mongo.conf.example

%files doc
%doc %{gem_docdir}

%changelog
* Mon Feb 11 2013 Krishna Raman <kraman@gmail.com> 1.1.3-1
- Merge pull request #1289 from
  smarterclayton/isolate_api_behavior_from_base_controller
  (dmcphers+openshiftbot@redhat.com)
- Merge branch 'improve_action_logging' into
  isolate_api_behavior_from_base_controller (ccoleman@redhat.com)
- change %%define to %%global (tdawson@redhat.com)
- Reading hostname from node.conf file instead of relying on localhost
  Splitting test features into common, rhel only and fedora only sections
  (kraman@gmail.com)
- Fixing init-quota to allow for tabs in fstab file Added entries in abstract
  for php-5.4, perl-5.16 Updated python-2.6,php-5.3,perl-5.10 cart so that it
  wont build on F18 Fixed mongo broker auth Relaxed version requirements for
  acegi-security and commons-codec when generating hashed password for jenkins
  Added Apache 2.4 configs for console on F18 Added httpd 2.4 specific restart
  helper (kraman@gmail.com)
- remove BuildRoot: (tdawson@redhat.com)
- make Source line uniform among all spec files (tdawson@redhat.com)
- Remove legacy login() method on authservice (ccoleman@redhat.com)
- All controllers should inherit the standard filters, except where they are
  bypassed (ccoleman@redhat.com)

* Mon Jan 28 2013 Krishna Raman <kraman@gmail.com> 1.1.2-1
- 875575 (dmcphers@redhat.com)
- Fix mongo auth plugin (rpenta@redhat.com)
- Bug 890119 (lnader@redhat.com)
- Moving model refactor work - Updated cartridge manifest files - Simplified
  descriptor - Switched from mongo gem to use mongoid (kraman@gmail.com)
- Ensure write to at least 2 mongo instances (dmcphers@redhat.com)
- Adding support for broker to mongodb connections over SSL
  (calfonso@redhat.com)

* Fri Jan 11 2013 Troy Dawson <tdawson@redhat.com> 1.1.1-1
- updated gemspecs so they work with scl rpm spec files. (tdawson@redhat.com)
- more changes for US3078 (abhgupta@redhat.com)
- fix elif typos (dmcphers@redhat.com)
- add oo-ruby (dmcphers@redhat.com)
- more ruby1.9 changes (dmcphers@redhat.com)
- add config to gemspec (dmcphers@redhat.com)
- Moving plugins to Rails 3.2.8 engine (kraman@gmail.com)
- getting specs up to 1.9 sclized (dmcphers@redhat.com)
- specifying rake gem version range (abhgupta@redhat.com)
- Bug 871436 - moving the default path for AUTH_PRIVKEYFILE and AUTH_PUBKEYFILE
  under /etc (bleanhar@redhat.com)
- fix an ss reference (dmcphers@redhat.com)
- Moving broker config to /etc/openshift/broker.conf Rails app and all oo-*
  scripts will load production environment unless the
  /etc/openshift/development marker is present Added param to specify default
  when looking up a config value in OpenShift::Config Moved all defaults into
  plugin initializers instead of separate defaults file No longer require
  loading 'openshift-origin-common/config' if 'openshift-origin-common' is
  loaded openshift-origin-common selinux module is merged into F16 selinux
  policy. Removing from broker %%postrun (kraman@gmail.com)
- BZ847976 - Fixing Jenkins integration (bleanhar@redhat.com)
- Fixed broker/node setup scripts to install cgroup services. Fixed
  mcollective-qpid plugin so it installs during origin package build. Updated
  cgroups init script to work with both systemd and init.d Updated oo-trap-user
  script Renamed oo-cgroups to openshift-cgroups (service and init.d) and
  created oo-admin-ctl-cgroups Pulled in oo-get-mcs-level and abstract/util
  from origin-selinux branch Fixed invalid file path in rubygem-openshift-
  origin-auth-mongo spec Fixed invlaid use fo Mcollective::Config in
  mcollective-qpid-plugin (kraman@gmail.com)

* Thu Oct 11 2012 Brenton Leanhardt <bleanhar@redhat.com> 0.8.9-1
- fix for mongo auth plugin spec file (abhgupta@redhat.com)
- Centralize plug-in configuration (miciah.masters@gmail.com)
- Removing old build scripts Moving broker/node setup utilities into util
  packages Fix Auth service module name conflicts (kraman@gmail.com)
- Merge pull request #613 from kraman/master (openshift+bot@redhat.com)
- Module name and gem path fixes for auth plugins (kraman@gmail.com)
