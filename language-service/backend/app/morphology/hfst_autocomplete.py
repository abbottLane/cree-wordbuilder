import re
import time
from hfst_optimized_lookup import TransducerFile
from subprocess import Popen, PIPE, STDOUT
import sys

class HFSTModel:
    def __init__(self, modelPath):
        super().__init__()
        self.modelPath = modelPath
        self.num_results = 15
       

    def apply_down(self, word):
        # do lookup
        start = time.time()        
        p = Popen(["hfst-optimized-lookup", "-q",  "-u", "-n", str(self.num_results), self.modelPath], stdout=PIPE, stdin=PIPE, stderr=STDOUT )
        results = p.communicate(input=word.encode('utf-8'))[0]
        print("RESULTS:\n" + results.decode())
        stop = time.time()
        print("INFO: model query time: " + str(stop-start))
        return [x.split('\t')[1] for x in results.decode().split('\n') if x != ""] # return a list of the second column entries


       


