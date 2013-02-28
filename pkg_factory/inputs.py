import argparse
import os
import platform

class Inputs(object):

    # Base location for any configuration files
    data_dir = "/etc/pkg-factory"

    # Dir where user-defined RPM build scripts are stored
    user_script_dir = "~/.pkg-factory-scripts"

    rpm_distros = ['fedora', 'SuSE', 'OpenSUSE', 'redhat', 'centos']
    deb_distros = ['debian', 'ubuntu']

    namespace = argparse.Namespace()
    
    def __init__(self):
        parser = argparse.ArgumentParser(prog='pkg-factory', description='Create a software deployment package using given parameters')
        
        # Enforce one source of package content
        pkg_source_group = parser.add_mutually_exclusive_group()
        pkg_source_group.add_argument("--local_base_dir",  metavar="<dir>",        help="Package content base directory")
        pkg_source_group.add_argument("--git_uri",    metavar="<URI>",        help="git repository URI with package source")
        
        parser.add_argument("pkg_name",                                     help="Package name")
        parser.add_argument("--arch",               metavar="<text>",       help="Package host architecture ('i686', 'x86_64' or 'noarch') - defaults to 'uname -m'")
	parser.add_argument("--build_dir",          metavar="<dir>",        help="Build directory - this is where temporary files and the created package are stored - defaults to ~/pkg_factory")
        parser.add_argument("--build_verbose",                              help="Enables verbose output of low level package build steps", action='store_true')
        parser.add_argument("--description",        metavar="<text>",       help="Package description")
        parser.add_argument("--license",            metavar="<text>",       help="Software license type (default = 'Free')")
        parser.add_argument("--package_group",      metavar="<text>",       help="Repo package group name (default = 'none')")
        parser.add_argument("--local_repo_dir",     metavar="<dir>",        help="Local repo directory - package will be copied here")
        parser.add_argument("--reset_build_script",                         help="Resets stored build script using given args", action='store_true')
        parser.add_argument("--reset_spec_file",                            help="Resets SPEC file using template", action='store_true')
        parser.add_argument("--requires",           metavar="<CSV>",        help="Comma separated list of required packages (dependencies)")
        parser.add_argument("--rsync_verbose",                              help="Enables verbose output of rsync", action='store_true')
        parser.add_argument("--summary",            metavar="<text>",       help="Package summary")
        parser.add_argument("--verbose",                                    help="Enables verbose output of high level processing", action='store_true')

        """ TODO: enable these future optional arguments
        --skip_build_script help="Don't create a build script allowing repeats of this build"
        --skip_build_script_alias help="Don't create a shell alias for the build script"
        """       
 
        parser.parse_args(namespace=self.namespace)

        """ Detect the linux distribution and set vars accordingly """
        distro_name, distro_version, distro_qualifier, distro_alias = platform.linux_distribution(full_distribution_name=False)
        for rpm_distro in self.rpm_distros:
            if rpm_distro == distro_name:
                self.namespace.package_type = 'rpm'
        
        for deb_distro in self.deb_distros:
            if deb_distro == distro_name:
                self.namepspace.package_type = 'deb'

        if self.namespace.package_type == 'rpm':
            template_cfg_file = self.data_dir + "/rpm_template.spec"
	
        """
        Below, default and conditional inputs are set based on the arguments parsed above.
        The intent here is to provide the Processor class with all the data it needs to do its job. 
        """
        if self.namespace.verbose == True:
            print "Package name: " + self.namespace.pkg_name

        if self.namespace.arch is None:
            self.namespace.arch = platform.machine()
            
        if self.namespace.verbose == True:
            print "Architecture: " + self.namespace.arch

	if self.namespace.build_dir is None:
            self.namespace.build_dir = os.path.expanduser("~") + "/pkg_factory"

        if self.namespace.verbose == True:
            print "Build dir: " + self.namespace.build_dir            

        # See if we're using a git repo as the package source
        if self.namespace.git_uri:
            if self.namespace.verbose == True:
                print "Creating package from git URI: " + self.namespace.git_uri

        # Default to local filesystem as the package source
        else:
            if self.namespace.local_base_dir is None:
                self.namespace.local_base_dir = os.path.expanduser("~") + "/" + self.namespace.pkg_name
        
            if self.namespace.verbose == True:
                print "Local filesystem base dir for package source: " + self.namespace.local_base_dir

        if self.namespace.description is None:
            self.namespace.description = self.namespace.pkg_name           

        if self.namespace.verbose == True:
            print "Descripton: " + self.namespace.description
            
        if self.namespace.package_group is None:
            self.namespace.package_group = 'none'

        if self.namespace.verbose == True:
            print "Package Group: " + self.namespace.package_group

	if self.namespace.package_type is 'rpm':
            rpm_spec_file_path = ""
	    rpm_build_dir = self.namespace.build_dir + "/BUILD"
            rpm_buildroot_dir = self.namespace.build_dir + "/BUILDROOT"
            rpm_rpms_dir = self.namespace.build_dir + "/RPMS/" + self.namespace.arch
            rpm_sources_dir = self.namespace.build_dir + "/SOURCES"
            rpm_srpms_dir = self.namespace.build_dir + "/SRPMS"

            if self.namespace.verbose == True:
                print "RPM build dir: " + rpm_build_dir
                print "RPM bulid root dir: " + rpm_buildroot_dir
                print "RPM sources dir: " + rpm_sources_dir
            
	if self.namespace.verbose == True:
            print "Package Type: " + self.namespace.package_type

        if self.namespace.license is None:
            self.namespace.license = 'Free'
        
        if self.namespace.verbose == True:
            print "License: " + self.namespace.license
            
        if self.namespace.summary is None:
            self.namespace.summary = self.namespace.pkg_name
            
        if self.namespace.verbose == True:
            print "Summary: " + self.namespace.summary

        self.namespace.pkg_full_name = self.namespace.pkg_name + '.' + self.namespace.arch
