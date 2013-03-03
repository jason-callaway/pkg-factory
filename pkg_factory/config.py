import argparse
import os
import platform

class Config(object):

    # Namespace where parsed argument properties are initially stored
    argparse_namespace = argparse.Namespace()

    # Supported dpkg-based distros
    deb_distros = ['debian', 'ubuntu']

    # Supported rpm-based distros
    rpm_distros = ['fedora', 'SuSE', 'OpenSUSE', 'redhat', 'centos']
    
    template_cfg_file = ""
    
        
    # Dir where user-defined RPM build scripts are stored
    user_script_dir = os.path.expanduser("~") + "/.pkg-factory-scripts"
    
    def __init__(self):
        self.parse_arguments()
        self.set_attributes()
    
    def create_build_dirs(self):

        path_list = [self.build_script_dir]

        if self.local_repo_dir:
            path_list.append(self.local_repo_package_dir)

        if self.package_type == 'deb':
            pass

        if self.package_type == 'rpm':
            path_list.extend([self.rpm_spec_dir, self.rpm_build_dir, self.rpm_build_root_dir, self.rpm_sources_dir, self.rpm_srpms_dir, self.rpm_rpms_dir])

        for path in path_list:
            if not os.path.exists(path):
                os.makedirs(path, 0700)


    def get_rpm_spec(self):

        content = ("Name: " + self.pkg_name + "\n"
                    "Version: 0.1 \n"
                    "Summary: " + self.summary + "\n"
                    "Group: " + self.package_group + "\n"
                    "License: " + self.license + "\n"
                    "BuildArch: " + self.arch + "\n"
                    "Release: 0 \n")

        if self.requires:
            content += "Requires: " + self.requires + "\n"
            if self.verbose:
                print "Requiring packages: " + self.requires

        if self.rpm_no_auto_requirements:
            
            content += ("\n# Do not interrogate package contents for shared library dependencies \n"
                        "AutoReqProv: no \n")

            if self.verbose:
                print "Skipping RPM auto requirement detection"

        content += "\n%description \n" + self.description + "\n"

        if self.rpm_no_strip_binaries:
            
            content += ("\n# Avoid binary stripping which alters md5 sums of binaries \n"
                        "%define __os_install_post %{nil} \n" 
                        "%install\n" 
                        "export DONT_STRIP=1\n\n")

            if self.verbose:
                print "Skipping RPM auto binary stripping"

        #include the "clean" stanza explicitly - supports older versions of rombuild
        content += ('%clean' + "\n"
                    'rm -rf %{buildroot}' + "\n\n")

        # include stub sections to be used by packagers independent of this utility
        content += ("%files\n" 
                    "%defattr(-,-,-)\n\n" 
                    "%preun\n" 
                    "%postun\n" 
                    "%pre\n" 
                    "%post\n")

        return content

    
    def parse_arguments(self):

        parser = argparse.ArgumentParser(prog='pkg-factory', description='Create a software deployment package using given parameters')
        
        # Enforce one source of package content
        pkg_source_group = parser.add_mutually_exclusive_group()
        pkg_source_group.add_argument("--local_base_dir",  metavar="<dir>",  help="Package content base directory")
        pkg_source_group.add_argument("--git_uri",    metavar="<URI>",       help="git repository URI with package source")
        
        parser.add_argument("pkg_name",                                     help="Package name")
        parser.add_argument("--arch",               metavar="<text>",       help="Package host architecture ('i686', 'x86_64' or 'noarch') - defaults to 'uname -m'")
        parser.add_argument("--build_dir",          metavar="<dir>",        help="Build directory - this is where temporary files and the created package are stored - defaults to ~/pkg_factory")
        parser.add_argument("--build_verbose",                              help="Enables verbose output of low level package building steps", action='store_true')
        parser.add_argument("--description",        metavar="<text>",       help="Package description")
        parser.add_argument("--license",            metavar="<text>",       help="Software license type (default = 'Free')")
        parser.add_argument("--local_repo_dir",     metavar="<dir>",        help="Local repo directory - package will be copied here")
        parser.add_argument("--package_group",      metavar="<text>",       help="Repo package group name (default = 'none')")
        parser.add_argument("--rpm_no_auto_requirements",                   help="(RPM only) Don't automatically scan package content for implicit requirements like shared libraries", action='store_true')
        parser.add_argument("--rpm_no_strip_binaries",                      help="(RPM only) Don't automatically strip binaries in package content", action='store_true')
        parser.add_argument("--save_build_script",                          help="Stores pkg-factory script using given arguments", action='store_true')
        parser.add_argument("--reset_config_file",                          help="Resets SPEC file using template", action='store_true')
        parser.add_argument("--requires",           metavar="<CSV>",        help="Comma separated list of required packages (dependencies)")
        parser.add_argument("--rsync_verbose",                              help="Enables verbose output of rsync", action='store_true')
        parser.add_argument("--summary",            metavar="<text>",       help="Package summary")
        parser.add_argument("--verbose",                                    help="Enables verbose output of high level processing", action='store_true')

        """ TODO: enable these future optional arguments
        --post_install_script=  look for as build/post_install by default - if it's there, copy it into the SPEC file
        --post_uninstall_script=
        --pre_install_script=
        --pre_uninstall_script=
        --version
        --release
        """      
        
        """TODO: make sure either local_base_dir or git_url is set... """
        parser.parse_args(namespace=self.argparse_namespace)
        
    def set_attributes(self):

        # Move all namespace attributes to this class
        namespace_keys = self.argparse_namespace.__dict__.keys()
        for key in namespace_keys:
            self.__dict__[key] = self.argparse_namespace.__dict__[key]
        
        # Don't need the temporary namespace anymore
        #del(self.argparse_namespace)

        """
        Below, default and conditional inputs are set based on the arguments parsed above.
        The intent here is to provide the Processor class with all the data it needs to do its job. 
        """

        """ Detect the linux distribution and set vars accordingly """
        distro_name, distro_version, distro_alias = platform.linux_distribution(full_distribution_name=False)
        for rpm_distro in self.rpm_distros:
            if rpm_distro == distro_name:
                self.package_type = 'rpm'
        
        for deb_distro in self.deb_distros:
            if deb_distro == distro_name:
                self.package_type = 'deb'

        if self.verbose :
            print "Package Type: " + self.package_type

        if self.verbose :
            print "Package name: " + self.pkg_name

        if not self.arch:
            self.arch = platform.machine()
            
        if self.verbose :
            print "Architecture: " + self.arch

        self.pkg_full_name = self.pkg_name + '.' + self.arch
        
        if self.verbose :
            print "Full package name: " + self.pkg_full_name

        if not self.build_dir:
            self.build_dir = os.path.expanduser("~") + "/pkg_factory"

        self.build_script_dir = self.build_dir + "/scripts"

        if self.verbose :
            print "Build dir: " + self.build_dir      

        if self.package_type == 'rpm':
            
            self.rpm_base_dir = self.build_dir + "/rpmbuild"
            self.rpm_spec_dir = self.rpm_base_dir + "/SPECS"
            self.rpm_spec_file = self.rpm_spec_dir + "/" + self.pkg_name + ".spec"
            self.rpm_build_dir = self.rpm_base_dir + "/BUILD"
            self.rpm_build_root_dir = self.rpm_base_dir + "/BUILDROOT"
            self.rpm_rpms_dir = self.rpm_base_dir + "/RPMS/" + self.arch
            self.rpm_sources_dir = self.rpm_base_dir + "/SOURCES"
            self.rpm_srpms_dir = self.rpm_base_dir + "/SRPMS"
            
            if self.local_repo_dir:
                self.local_repo_package_dir = self.local_repo_dir + "/Packages"
            
            if self.verbose :
                print "RPM build dir: " + self.rpm_build_dir
                print "RPM build root dir: " + self.rpm_build_root_dir
                print "RPM sources dir: " + self.rpm_sources_dir
                print "SRPM dir: " + self.rpm_srpms_dir
            
        if self.package_type == 'deb':
            pass

        if self.reset_config_file  and self.verbose :
            print "Resetting package config file"

        """ See if we're using a git repo as the package source """
        if self.git_uri and self.verbose :
            print "Creating package from git URI: " + self.git_uri

        # Default to local filesystem as the package source
        else: 
            if not self.local_base_dir:
                self.local_base_dir = os.path.expanduser("~") + "/" + self.pkg_name
        
            if self.verbose:
                print "Local filesystem base dir for package source: " + self.local_base_dir

        if not self.description:
            self.description = self.pkg_name           

        if self.verbose:
            print "Descripton: " + self.description
            
        if not self.package_group:
            self.package_group = 'none'

        if self.verbose:
            print "Package Group: " + self.package_group

        if not self.license:
            self.license = 'Free'
        
        if self.verbose :
            print "License: " + self.license
            
        if not self.summary:
            self.summary = self.pkg_name

        if self.verbose :
            print "Summary: " + self.summary       

        if self.save_build_script:
            self.build_script_path = self.build_script_dir + "/" + self.pkg_name


 