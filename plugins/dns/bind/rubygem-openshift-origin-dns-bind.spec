%if 0%{?fedora}%{?rhel} <= 6
    %global scl ruby193
    %global scl_prefix ruby193-
%endif
%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}
%global gem_name openshift-origin-dns-bind
%global rubyabi 1.9.1

Summary:       OpenShift plugin for BIND service
Name:          rubygem-%{gem_name}
Version:       1.1.1
Release:       1%{?dist}
Group:         Development/Languages
License:       ASL 2.0
URL:           http://openshift.redhat.com
Source0:       http://mirror.openshift.com/pub/openshift-origin/source/%{gem_name}/rubygem-%{gem_name}-%{version}.tar.gz
Requires:      %{?scl:%scl_prefix}ruby(abi) = %{rubyabi}
Requires:      %{?scl:%scl_prefix}ruby
Requires:      %{?scl:%scl_prefix}rubygems
Requires:      %{?scl:%scl_prefix}rubygem(json)
Requires:      %{?scl:%scl_prefix}rubygem(dnsruby)
Requires:      rubygem(openshift-origin-common)
Requires:      bind
Requires:      bind-utils
Requires:      openshift-origin-broker
Requires:      selinux-policy-targeted
Requires:      policycoreutils-python
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
Obsoletes:     rubygem-uplift-bind-plugin

%description
Provides a Bind DNS service based plugin

%prep
%setup -q

%build
%{?scl:scl enable %scl - << \EOF}
mkdir -p ./%{gem_dir}
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
# gem install compiles any C extensions and installs into a directory
# We set that to be a local directory so that we can move it into the
# buildroot in %%install
gem install -V \
        --local \
        --install-dir ./%{gem_dir} \
        --bindir ./%{_bindir} \
        --force \
        --rdoc \
        %{gem_name}-%{version}.gem
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

# Add documents/examples
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}/
cp -r doc/* %{buildroot}%{_docdir}/%{name}-%{version}/

#Config file
mkdir -p %{buildroot}/etc/openshift/plugins.d
cp %{buildroot}/%{gem_dir}/gems/%{gem_name}-%{version}/conf/openshift-origin-dns-bind.conf.example %{buildroot}/etc/openshift/plugins.d/openshift-origin-dns-bind.conf.example

# Compile SELinux policy
mkdir -p %{buildroot}/usr/share/selinux/packages/rubygem-openshift-origin-dns-bind
cp %{buildroot}%{gem_dir}/gems/openshift-origin-dns-bind-*/doc/examples/dhcpnamedforward.* %{buildroot}/usr/share/selinux/packages/rubygem-openshift-origin-dns-bind

%files
%doc %{gem_docdir}
%doc %{_docdir}/%{name}-%{version}
%{gem_instdir}
%{gem_spec}
%{gem_cache}
/usr/share/selinux/packages/rubygem-openshift-origin-dns-bind
/etc/openshift/plugins.d/openshift-origin-dns-bind.conf.example


%changelog
* Fri Jan 11 2013 Troy Dawson <tdawson@redhat.com> 1.1.1-1
- updated gemspecs so they work with scl rpm spec files. (tdawson@redhat.com)
- F18 compatibility fixes   - apache 2.4   - mongo journaling   - JDK 7   -
  parseconfig gem update Bugfix for Bind DNS plugin (kraman@gmail.com)
- add config to gemspec (dmcphers@redhat.com)
- Moving plugins to Rails 3.2.8 engine (kraman@gmail.com)
- getting specs up to 1.9 sclized (dmcphers@redhat.com)
- specifying rake gem version range (abhgupta@redhat.com)
- Moving broker config to /etc/openshift/broker.conf Rails app and all oo-*
  scripts will load production environment unless the
  /etc/openshift/development marker is present Added param to specify default
  when looking up a config value in OpenShift::Config Moved all defaults into
  plugin initializers instead of separate defaults file No longer require
  loading 'openshift-origin-common/config' if 'openshift-origin-common' is
  loaded openshift-origin-common selinux module is merged into F16 selinux
  policy. Removing from broker %%postrun (kraman@gmail.com)

* Tue Oct 23 2012 Brenton Leanhardt <bleanhar@redhat.com> 0.8.12-1
- removing remaining cases of SS and config.ss (dmcphers@redhat.com)
- Making openshift-origin-msg-broker-mcollective a Rails engine so that it can
  hook into Rails initializers Making openshift-origin-dns-bind a Rails engine
  so that it can hook into Rails initializers (kraman@gmail.com)
