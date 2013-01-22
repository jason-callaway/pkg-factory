#!/bin/bash

. /opt/rpm-factory/include/include_vars.sh

if [ ! -d $RF_BUILD_DIR ]; then        mkdir -p $RF_BUILD_DIR; fi
if [ ! -d $RF_BUILD_RPM_DIR ]; then    mkdir -p $RF_BUILD_RPM_DIR; fi
if [ ! -d $RF_BUILD_SCRIPT_DIR ]; then mkdir -p $RF_BUILD_SCRIPT_DIR; fi
if [ ! -d $RF_BUILD_SPEC_DIR ]; then   mkdir -p $RF_BUILD_SPEC_DIR; fi

ln -s /opt/rpm-factory/scripts/rpm-factory /usr/sbin/rpm-factory
