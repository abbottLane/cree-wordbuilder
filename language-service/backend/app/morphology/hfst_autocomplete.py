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


    def _clean_ranked_hfst_results(self, results):
        # start = time.time()
        results = [(re.sub("\@.*?\@", "", x[0]), x[1]) for x in list(results)] # strip out flag diacritics
        # stop = time.time()
        # print("DIA: " + str(stop-start))
        
        # remove duplicates while preserving ranked order
        # start  = time.time()
        seen = {}
        deduped_results = []
        for r in results:
            if r[0] not in seen:
                deduped_results.append(r[0]) #  + "::" + str(r[1]) <-- for debugging weights
                seen[r[0]] = r[1]
        # return clean results
        # stop = time.time()
        # print("Dedupe: " + str(stop-start))

        return deduped_results

    def apply_down(self, word):

        # do lookup
        # start = time.time()
        results = list(self.fst.lookup(word, max_number=25))
        # stop = time.time()
        # print("LOOKUP: " + str(stop-start))

        return self._clean_ranked_hfst_results(results) # lookup word

