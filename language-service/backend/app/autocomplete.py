from logging import NullHandler
from app.morphology.fst import process_autocomplete_query
from app.dictionary.search import entries_by_results
from typing import Dict, Tuple, List
import logging
logging.basicConfig(level=logging.INFO)

async def search(searchdata: Dict) -> Tuple[List[str], int, Tuple[List[str], List[str], int]]:
    logging.info("Completion Query: " + searchdata['search'])
    limit = searchdata['limit'] if searchdata['limit'] else 10
    results = await process_autocomplete_query(searchdata['search'])
    # check each result to see if it is valid for analysis
    annotated_results = []
    for i,r in enumerate(results[:limit]):        
        annotated_results.append((r, False, "", r))
        
    return (list(set(annotated_results)), len(results), None)

def make_readable_result(r):
    return r['english'] #r['analyzed_form'] #+ "\n" + r['english']
