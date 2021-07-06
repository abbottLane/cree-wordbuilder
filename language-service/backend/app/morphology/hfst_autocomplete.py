import hfst
import re
import time
import pexpect
import sys

class HFSTModel:
    def __init__(self, modelPath):
        super().__init__()
        self.modelPath = modelPath
        hfst.set_default_fst_type(hfst.ImplementationType.HFST_OLW_TYPE)
        self.hfst_process = hfst.HfstInputStream(self.modelPath)
        self.fst = self.hfst_process.read()
        self.num_results = 25
       

    def apply_down(self, word):
        # do lookup
        start = time.time()
        results = self.fst.lookup(word)[:self.num_results]
        # print("RESULT::::" + str(results))
        results = [re.sub("\@.*?\@", "", x[0]) + " " + str(x[1]) for x in results] # strip out flag diacritics
        stop = time.time()
        print("INFO: model query time: " + str(stop-start))
        return results


       


