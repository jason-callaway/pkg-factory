'''
Created on Feb 27, 2013

@author: joe
'''
import os
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
        
        if self.config.package_type == 'deb':
            print "Debian package building not yet implemented"
            sys.exit(1)

        elif self.config.package_type == 'rpm':           

            self.do_build_rpm()
    
        else:
            print "Package type not supported: " + self.config.package_type
            sys.exit(3);
        
        

            
        
        
        """
         Copy the created package to a local repository, resolving any missing dependencies
         like directory creation
        """
#        if self.config.local_repo_dir:
#            copy(self.config.rpm_file_path, self.config.local_repo_dir)

        
            



        if self.config.save_build_script:
            self.save_build_script()
            
        sys.exit(0)

    def do_build_deb(self):
        pass
    
    def do_build_rpm(self):

        # Update or create the SPEC file as needed
        if os.path.exists(self.config.rpm_spec_file) and self.config.reset_config_file is not True:

            print "RPM SPEC file exists: " + self.config.rpm_spec_file + " - updating"
            spec_file_handle = open(self.config.rpm_spec_file)
            spec_file_content = spec_file_handle.read()
            
            #TODO: modify spec file in place with new version number(s)
            
            

        else:
            print "Creating RPM SPEC file: " + self.config.rpm_spec_file + " from template"
            
            try:
                spec_file_handle = open(self.config.rpm_spec_file, 'w+')
                spec_file_handle.write(self.config.get_rpm_spec())
                spec_file_handle.close()

            except Exception as e:
                print "Could not create RPM SPEC file: " + self.config.rpm_spec_file + ": " + e.strerror 
                sys.exit(2)
                    
        # do the rsync here (if needed)
        # do the package build here
        try:
            
            rpmbuild_args = [
                             'rpmbuild',
                             '-bb',
                             '--target=' + self.config.arch,
                             '--buildroot='+ self.config.rpm_build_root_dir,
                             self.config.rpm_spec_file
                             ]
            
            if not self.config.build_verbose:
                rpmbuild_args.append('--quiet')

            subprocess.check_call(rpmbuild_args)
            #TODO: something with the rpmbuild cmd output - check self.config.verbose
            
        except subprocess.CalledProcessError as e:
            
            print "Failed to build RPM"
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
"""        
        


# configure version info of this particular build
typeset -i old_release_num=`grep 'Release:' $rpm_spec_file | cut -d' ' -f2 | cut -d'.' -f1`
typeset -i new_release_num=$old_release_num+1
new_release="${new_release_num}.$RF_DISTRO"
build_version="`grep 'Version: ' $rpm_spec_file | cut -d' ' -f2`-$new_release"
# configure metadata for rpm-build


build_name="${rpm_name}-${build_version}.${rpm_arch}"



rpm_file="$RF_BUILD_RPM_DIR/$rpm_arch/${build_name}.rpm"

# auto-increment the release/build number in the SPEC file
echo "Using release number: $new_release"
sed -i -e "s/^Release:.*/Release: $new_release/g" $rpm_spec_file

echo "Cleaning build dir"
rm -rf $build_base/$rpm_mask
rm -rf $build_home
mkdir -p $build_home

# since rpm-factory is designed for building packages from pre-compiled or no source,
# all we need to to is rsync the base dir into a build directory for packaging.
rsync \
--exclude=".git*" \
--exclude=".*.swp*" \
--exclude=".svn*" \
--exclude="nbproject/*" \
$rsync_quiet \
-avvE $basedir/ $build_home

if [ $? -ne 0 ]; then
    
    echo "rsync from $basedir to $build_home failed."
    rf_exit 1
fi

# All prep work should be complete; build the package and move any older ones into a history
# subdir.
echo "Running rpmbuild"
echo "  SPEC file: $rpm_spec_file"
if [ ! -d $rpm_base/history ]; then mkdir -p $rpm_base/history; fi
mv $rpm_base/$rpm_mask $rpm_base/history/ >/dev/null 2>&1

# call rpmbuild to make the RPM
rpmbuild \
-bb \
-buildroot=$build_home \
--target=$rpm_arch \
$rpmbuild_quiet \
$rpm_spec_file



# Copy the package to the repository (if given) and rebuild its metadata
if [ "$repo_dir" ]; then

    repo_pkg_dir=$repo_dir/Packages

    if [ ! -d $repo_pkg_dir ]; then

        echo "Creating $repo_pkg_dir"
        mkdir -p $repo_pkg_dir
    fi

    echo "Copying RPM file to repo"
    echo "  $rpm_file => $repo_pkg_dir"
    cp $rpm_file $repo_pkg_dir
    cd $repo_dir
    createrepo ./
fi
"""
