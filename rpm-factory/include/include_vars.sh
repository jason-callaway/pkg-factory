#!/bin/bash

export RF_BASE_DIR=/opt/rpm-factory
export RF_DATA_DIR=$RF_BASE_DIR/data
export RF_SCRIPT_DIR=$RF_BASE_DIR/scripts
export RF_INCLUDE_DIR=$RF_BASE_DIR/include

. $RF_INCLUDE_DIR/include_funcs.sh

# Default macros file
export RF_DEFAULT_RPM_MACROS=$RF_DATA_DIR/rpmmacros

# Directories for rpm build
export RF_BUILD_ROOT="/root/rpmbuild"
export RF_BUILD_DIR=$RF_BUILD_ROOT/BUILD
export RF_BUILD_SCRIPT_DIR=$RF_BUILD_ROOT/SCRIPTS
export RF_BUILD_SPEC_DIR=$RF_BUILD_ROOT/SPECS
export RF_BUILD_RPM_DIR=$RF_BUILD_ROOT/RPMS

# SPEC file template
export RF_TEMPLATE_SPEC_FILE=$RF_DATA_DIR/template.spec

# Distribution name tag (for RPM naming)
export RF_ARCH=`uname -i`
export RF_DISTRO=`uname -r | sed -e "s/\.$RF_ARCH//" | sed -e "s/^.*\.//"`
