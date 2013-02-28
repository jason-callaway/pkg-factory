'''
Created on Feb 27, 2013

@author: joe
'''

class Processor(object):
    '''        
    classdocs
    '''

    inputs = None
    
    def __init__(self, inputs):
        self.inputs = inputs
        
    def main(self):

        


	if inputs.package_type == 'rpm':

            # Update or create the SPEC file as needed
            if os.path.exists(inputs.rpm_spec_file_path):
                if inputs.verbose == True:
                    print "RPM SPEC file exists: " + inputs.rpm_spec_file_path + " - updating"

                spec_file_handle = open(inputs.rpm_spec_file_path)
                spec_file_content = spec_file_handle.read()

	else:
            print "Package type not supported: ".inputs.package_type
        
        
        #my_config = Config()
        #with open(my_config.spec_template) as f:
        #spec_content = f.read()

"""        
        
        echo "Configuring any unset but required vars for build: $RPM_FULL_NAME"


rpm_mask="${rpm_name}-[0-9]*.${RF_DISTRO}.${rpm_arch}.rpm"
rpm_spec_file=$RF_BUILD_SPEC_DIR/${rpm_name}.${RF_DISTRO}.${rpm_arch}.spec
rpm_build_script=$RF_BUILD_SCRIPT_DIR/build_${rpm_name}.sh

# create the RPM SPEC file using the given args (as transformed into vars)
if [[ ! -e $rpm_spec_file || "$reset_spec_file" == "TRUE" || "$reset_spec_file" == "true" ]]; then

    echo "Creating SPEC file ($rpm_spec_file) from template"
    cat $RF_TEMPLATE_SPEC_FILE \
    | sed -e "s/#ARCH/$rpm_arch/g" \
    | sed -e "s=#DESCRIPTION=$description=g" \
    | sed -e "s,#DISTRO,$RF_DISTRO,g" \
    | sed -e "s/#GROUP/$pkg_group/g"  \
    | sed -e "s=#LICENSE=$license=g"  \
    | sed -e "s/#REQUIRES/$requires/g" \
    | sed -e "s,#RPM_DIR,$basedir,g"  \
    | sed -e "s/#RPM_NAME/$rpm_name/g" \
    | sed -e "s=#SUMMARY=$summary=g" \
     > $rpm_spec_file

    # If there are any package requirements (dependencies), enable them
    if [ "$requires" ]; then
        sed -i -e "s/^#Requires:/Requires:/" $rpm_spec_file
    fi
fi

# create a package skeleton if the base dir does not exist - gives the devekioer
# a head start
if [ ! -d $basedir ]; then

    echo "Creating $basedir"
    mkdir -p $basedir

    echo "Creating RPM skeleton using rpm-factory defaults"
    mkdir -p $basedir/scripts $basedir/include $basedir/data
    touch $basedir/scripts/rpm_preun.sh
    touch $basedir/scripts/rpm_post.sh
    touch $basedir/scripts/rpm_postun.sh
fi

# create a build script which captures this usage of rpm-factory
if [[ ! -e $rpm_build_script || "$reset_build_script" == "TRUE" || "$reset_build_script" == "true" ]]; then

    echo "Creating RPM build script from given args ($rpm_build_script)"
    cat $RF_DATA_DIR/template.sh > $rpm_build_script

    # keep track of the number of args
    typeset -i count=0

    # process the argument list as key/value pairs and concatenate them to the build script
    while read arg; do

            # extract the variable name & value
            var=`echo "$arg" | sed -e "s/^--//" | sed -e "s/=.*//"`
            value=`echo "$arg" | sed -e "s/^--.*=//"`

        if [ "$var" ]; then

            count=$count+1
    
            # capture anything but a "reset" argument
            if [[ "$var" != "reset"* ]]; then

                # capture the argument so we can re-use it
                arg="--${var}=\"${value}\""
    
                # if we're not the last arg, include a continuous line indicator character ('\') 
                if [ $save_arg_count -ne $count ]; then
                    arg="$arg \\"
                fi

                echo "$arg" >> $rpm_build_script
            fi
        fi

    done < $RF_TMPFILE

    chmod 550 $rpm_build_script
fi

# configure version info of this particular build
typeset -i old_release_num=`grep 'Release:' $rpm_spec_file | cut -d' ' -f2 | cut -d'.' -f1`
typeset -i new_release_num=$old_release_num+1
new_release="${new_release_num}.$RF_DISTRO"
build_version="`grep 'Version: ' $rpm_spec_file | cut -d' ' -f2`-$new_release"
# configure metadata for rpm-build
build_name="${rpm_name}-${build_version}.${rpm_arch}"
build_base="$RF_BUILD_ROOT/BUILDROOT"
build_dir="${build_base}/${build_name}"
build_home="${build_dir}/${basedir}"
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

# Evaluate success of the rpm build
if [ $? -ne 0 ]; then

    echo "rpmbuild command failed"
    rf_exit 2
fi

# Create an alias so we could build this RPM again quickly if desired
alias_file="~/.bashrc"
alias_name="build_${rpm_name}"
echo "Adding alias: $alias_name to $alias_file"
echo "  To re-run this build, source $alias_file then execute '$alias_name' from the shell"
sed -i -e "/^alias $alias_name=.*$/d" $alias_file
echo "alias $alias_name='$rpm_build_script'" >> $alias_file

# Copy the package to an archive destination (if given) and move any older packages into a history dir
if [ "$archive_server_ip" ]; then

    if [ ! "$archive_server_dir" ]; then

        archive_server_dir=/var/tmp
    fi

    echo "Copying $rpm_mask to $archive_server_ip:$archive_server_dir"
    ssh -q $archive_server_ip "mkdir -p $archive_server_dir/history"
    ssh -q $archive_server_ip "mv $archive_server_dir/$rpm_mask $archive_server_dir/history"
    scp $rpm_file $archive_server_ip:$archive_server_dir

fi

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
