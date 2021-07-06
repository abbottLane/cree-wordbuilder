import hfst
import re
import time

class HFSTModel:
    def __init__(self, modelPath):
        super().__init__()
        self.modelPath = modelPath
        hfst.set_default_fst_type(hfst.ImplementationType.HFST_OLW_TYPE)
        self.hfst_process = hfst.HfstInputStream(self.modelPath)
        self.fst = self.hfst_process.read()

    def apply_down(self, word):
        # do lookup
        # start = time.time()
        results = [x for x in self.fst.lookup(word, max_number=50)]
        print("RESULT::::" + str(results))
        results = [re.sub("\@.*?\@", "", x[0]) + " " + str(x[1]) for x in results] # strip out flag diacritics
        # stop = time.time()
        return results

