#!/usr/bin/python

from pkg_factory.processor import Processor
from pkg_factory.inputs import Inputs

""" test block """
import sys
sys.argv.append("--verbose")
sys.argv.append("--arch=noarch")
sys.argv.append("--description=my description")
#sys.argv.append("--git_uri=ssh://git@gitlab.maderj.com:pkg_factory.git")
sys.argv.append("--local_base_dir=/my/package/location")

sys.argv.append("mypackage")
""" end test block """

processor = Processor(inputs=Inputs().namespace)
processor.main()