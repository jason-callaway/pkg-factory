import os
import platform

class Processor:
    
    inputs = None
    
    def __init__(self, inputs):
        self.inputs = inputs
    
    def main(self):
        print platform.machine()
        print platform.node()
  
myProcessor = Processor(inputs=None)      
myProcessor.main()