import Config
import os
import platform

class Processor:
    
    inputs = None
    
    def __init__(self, inputs):
        self.inputs = inputs
    
    def main(self):
        #print platform.machine()
        #print platform.node()
        #rpm_full_name = self.inputs.rpm_name + platform.machine()
        rpm_full_name = "foo" + '.' + platform.machine()
        
        print rpm_full_name
        
        my_config = Config()
        with open(my_config.spec_template) as f:
            spec_content = f.read()