#!/usr/bin/python

from pkg_factory.processor import Processor
from pkg_factory.inputs import Inputs

processor = Processor(inputs=Inputs().namespace)
processor.main()