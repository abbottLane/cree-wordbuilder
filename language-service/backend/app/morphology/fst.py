import re
from re import DEBUG
import time
from app.morphology.hfst_autocomplete import HFSTModel

completions = HFSTModel('app/morphology/crk-infl-morpheme-completion.weighted.hfstol')


async def process_autocomplete_query(query_text):
    results = []
    if query_text:
        query_text = query_text.split()[0]
        query_text = re.sub("^", "", query_text)

        start = time.time()
        results = completions.apply_down(query_text)
        end = time.time()

    return results
