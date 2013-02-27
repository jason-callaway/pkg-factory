import os

class Config:

    # Base location for any configuration files
    data_dir = "/etc/rpm-factory"
    
    # Dir where user-defined RPM build scripts are stored
    user_script_dir = "~/.rpm-factory-scripts"
    
    # Default macros file (template)
    default_macros = data_dir + "/default_rpmmacros"
    
    # Template SPEC file
    spec_template = data_dir + "/template.spec"

    # Directories for rpm build
    storage_dir = "/var/lib/rpm-factory"
    build_dir = storage_dir + "/BUILD"
    srpm_dir  = storage_dir + "/SRPMS"
    spec_dir  = storage_dir + "/SPECS"
    rpm_dir   = storage_dir + "/RPMS"
    
    # list of all the storage dirs (used mainly for deploying rpm-factory)
    storage_dirs = [ build_dir, srpm_dir, spec_dir, rpm_dir ]

    def __init__(self):
        print "here" #pass
        
    def install(self):

        for path in self.storage_dirs:
            if not os.path.isdir(path):
                os.makedirs(path)