Summary: #SUMMARY
Name: #RPM_NAME
Version: 0.1
Group: #GROUP
Release: 0.#DISTRO
License: #LICENSE
BuildArch: #ARCH
#Requires: #REQUIRES

# Do not interrogate package contents for shared library dependencies. This can get ugly.
AutoReqProv: no

# Only sure-fire way to avoid binary stripping which alters md5 sums of binaries
%define __os_install_post %{nil}

%description
#DESCRIPTION

%install
# Another way to ensure binary stripping doesn't occur
export DONT_STRIP=1

%clean
# this stanza kept intentionally empty to allow packaging of content to el5 build hosts
# this will override the built-in function of rpm-build which deletes the BUILDROOT/<package name> dir

%files
%defattr(-,-,-)
#RPM_DIR

%preun

%postun

%pre

%post
