import hfst
import re
import time

class HFSTModel:
    def __init__(self, modelPath):
        super().__init__()
        self.modelPath = modelPath
        self.hfst_process = hfst.HfstInputStream(self.modelPath)
        self.fst = self.hfst_process.read()
        # print(help(self.fst))


    def apply_down(self, word):

        # do lookup
        # start = time.time()
        results = [x for x in self.fst.lookup(word, max_number=30)]
        results = [re.sub("\@.*?\@", "", x[0]) for x in results] # strip out flag diacritics
        # stop = time.time()
        # print("LOOKUP: " + str(stop-start))

        return results

