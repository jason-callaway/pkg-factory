Summary: Tools for rapid building of RPM packages
Name: RPM Factory
Version: 0.1
Release: 1.fc18
License: GPLv3
BuildArch: noarch
Requires: rpm-build, python >= 2.7.3

# Do not interrogate package contents for shared library dependencies. This can get ugly.
AutoReqProv: no

# Only sure-fire way to avoid binary stripping which alters md5 sums of binaries
%define __os_install_post %{nil}

%description
Tools for rapid building of RPM packages

%install
# Another way to ensure binary stripping doesn't occur
export DONT_STRIP=1

%clean
# this stanza kept intentionally empty to allow packaging of content to el5 build hosts
# this will override the built-in function of rpm-build which deletes the BUILDROOT/<package name> dir

#%files
#%defattr(-,-,-)
/etc/rpm-factory/
/usr/bin/rpm-factory
/usr/lib/python2.7/site-packages/rpm-factory

%preun	


%postun


%pre


%post
#!/usr/bin/python

from rpm_factory import config
my_config = config()
my_config.install()