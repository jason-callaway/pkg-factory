#!/usr/bin/python

from pkg_factory.processor import Processor
from pkg_factory.config import Config

""" test block """
import sys
sys.argv.append("--build_verbose")
#sys.argv.append("--verbose")
#sys.argv.append("--arch=noarch")
sys.argv.append("--local_repo_dir=/var/tmp/foobar")
sys.argv.append("--summary=my test package summary guy")
#sys.argv.append("--reset_config_file")
sys.argv.append("--rpm_no_auto_requirements")
sys.argv.append("--rpm_no_strip_binaries")
sys.argv.append("--description=my description")
sys.argv.append("--save_build_script")
#sys.argv.append("--release=56")
sys.argv.append("--version=3.6")

#sys.argv.append("--git_uri=ssh://git@gitlab.maderj.com:pkg_factory.git")
sys.argv.append("--local_base_dir=/var/tmp/foopkg")

sys.argv.append("mypackage")
""" end test block """

processor = Processor(config=Config())
processor.main()
