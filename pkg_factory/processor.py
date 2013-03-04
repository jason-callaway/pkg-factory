'''
Created on Feb 27, 2013

@author: joe
'''
import os
import shutil
import subprocess
import sys


class Processor(object):
    '''        
    classdocs
    '''

    config = None
    
    def __init__(self, config):
        self.config = config
        
    def main(self):
        
        # Create all the necessary dirs for the package build if they don't already exist
        self.config.create_build_dirs()
        
        # Call the dpkg handler
        if self.config.package_type == 'deb':
            self.build_deb()

        # Call the rpm handler
        elif self.config.package_type == 'rpm':           
            self.build_rpm()
    
        # Bail out - unsupported mode
        else:
            print "Package type not supported: " + self.config.package_type
            sys.exit(3);
        
        if self.config.save_build_script:
            self.save_build_script()
            
        sys.exit(0)

    def build_deb(self):
        print "Debian package building not yet implemented"
        sys.exit(1)
    
    def build_rpm(self):

        # Write the updated (or newly created) SPEC file
        try:

            rpm_spec_file_handle = open(self.config.rpm_spec_file_path, 'w')
            rpm_spec_file_handle.write(self.config.rpm_spec_content)
            rpm_spec_file_handle.close()
            
        except TypeError as e:

            print "Could not write RPM SPEC file: " + self.config.rpm_spec_file_path + ": " + e.message 
            sys.exit(2)

                    
        # rsync the package content into the build root
        try:

            rsync_args = ['rsync',
                          '-acE',
                          '--exclude=.git*',
                          '--exclude=".*.swp*',
                          '--exclude=".svn*',
                          '--exclude="nbproject/*']
            
            if self.config.build_verbose:
                rsync_args.append('-vv')
            else:
                rsync_args.append('-q')
            
            rsync_args.append(self.config.local_base_dir + "/")    
            rsync_args.append(self.config.rpm_build_root_dir + "/" + self.config.pkg_full_name)
                
            if self.config.verbose:
                rsync_command = ""
                
                for arg in rsync_args:
                    rsync_command += arg + " "
                
                print "Calling: " + rsync_command
                
            print "Synching build root with package content"
            subprocess.check_call(rsync_args)
        
        except subprocess.CalledProcessError as e:

            print "Failed to rsync package content into build root"
            print " exited with return code: " + str(e.returncode)
            sys.exit(4)
        
        
        # do the package build
        try:
            
            rpmbuild_args = ['rpmbuild', '-bb',
                             #'--buildroot='+ self.config.rpm_build_root_dir,
                             "--define=_topdir " + self.config.rpm_top_dir,
                             #'--target=' + self.config.arch,
                             self.config.rpm_spec_file_path]
            
            if not self.config.build_verbose:
                rpmbuild_args.append('--quiet')

            if self.config.verbose:
                rpmbuild_command = ""
                
                for arg in rpmbuild_args:
                    rpmbuild_command += arg + " "
                
                print "Calling: " + rpmbuild_command

            print "Building package"
            subprocess.check_call(rpmbuild_args)
            
        except subprocess.CalledProcessError as e:
            
            print "Failed to build RPM"
            print " exited with return code: " + str(e.returncode)
            sys.exit(5)

        # Copy the created package to a local repository, creating directories as needed
        if self.config.local_repo_dir:
            
            if not os.path.exists(self.config.local_repo_package_dir):
                os.makedirs(self.config.local_repo_package_dir)

            shutil.copy2(self.config.rpm_file_path, self.config.local_repo_package_dir)
            
            #TODO: think about implementing this natively in python, but that could trigger code churn here from upstream...
            try:
            
                createrepo_args = ['createrepo', self.config.local_repo_dir]
                subprocess.check_call(createrepo_args)
                
            except subprocess.CalledProcessError as e:
                
                print "Failed to build RPM repository metadata"
                print " exited with return code: " + str(e.returncode)
                sys.exit(4)


    def save_build_script(self):
        content = "pkg-factory \\ \n"
        for key,arg in enumerate(sys.argv):
            if key > 0 and arg != "--save_build_script":
                content += arg + " \\ \n "
        
        try: 
            spec_file_handle = open(self.config.build_script_path, 'w+')
            spec_file_handle.write(content)
        except Exception as e:
            print "Could not create package build script: " + self.config.build_script_path + ": " + e.strerror 
            sys.exit(2)
            
        print "Saved build script as " + self.config.build_script_path

