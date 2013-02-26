import argparse

class Inputs:

    namespace = argparse.Namespace()
    
    def __init__(self):
        parser = argparse.ArgumentParser(prog='rpm-factory', description='Create an RPM using given parameters')
        parser.add_argument("rpm_name", help="RPM name")
        parser.add_argument("rpm_arch", help="RPM host architecture ('i686', 'x86_64' or 'noarch')")
        
        parser.add_argument("--archive_server_ip",  metavar="<IP Address>", help="Archive Server IP address")
        parser.add_argument("--archive_server_dir", metavar="<dir>",        help="Archive Server directory")
        parser.add_argument("--basedir",            metavar="<dir>",        help="RPM content base directory")
        parser.add_argument("--description",        metavar="<text>",       help="RPM description (recommend encasing arg in quotes)")
        parser.add_argument("--license",            metavar="<text>",       help="Software license type (default = 'Free')")
        parser.add_argument("--package_group",      metavar="<text>",       help="Repo package group name (default = 'none')")
        parser.add_argument("--repo_dir",           metavar="<dir>",        help="Repo directory to copy built RPM")
        parser.add_argument("--reset_build_script", help="Resets stored build script using given args", action='store_true')
        parser.add_argument("--reset_spec_file",    help="Resets SPEC file using template", action='store_true')
        parser.add_argument("--requires",           metavar="<CSV>",        help="Comma separated list of required RPMs")
        parser.add_argument("--rpmbuild_verbose",   help="Enables verbose output of rpmbuild", action='store_true')
        parser.add_argument("--rsync_verbose",      help="Enables verbose output of rsync", action='store_true')
        parser.add_argument("--summary",            metavar="<text>",       help="RPM summary (recommend encasing arg in quotes)")
        
        if self.namespace.basedir is None:
            self.namespace.basedir = "/opt/" + self.namespace.rpm_name
        
        if self.namespace.description is None:
            self.namespace.description = self.namespace.rpm_name
            
        if self.namespace.package_group is None:
            self.namespace.package_group = 'none'
            
        if self.namespace.license is None:
            self.namespace.license = 'Free'
            
        if self.namespace.summary is None:
            self.namespace.summary = self.namespace.rpm_name
        
        
        
        
        print self.namespace.basedir
        #parser.print_help()

        
    
Inputs()