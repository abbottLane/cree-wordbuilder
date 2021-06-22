from logging import NullHandler
from app.morphology.fst import process_autocomplete_query
from typing import Dict, Tuple, List
import logging
logging.basicConfig(level=logging.INFO)

async def search(searchdata: Dict) -> Tuple[List[str], int, Tuple[List[str], List[str], int]]:
    logging.info("Completion Query: " + searchdata['search'])
    limit = searchdata['limit'] if searchdata['limit'] else 10
    results = await process_autocomplete_query(searchdata['search'])
    
    # dedupe
    annotated_results = []
    res_set = set()
    for i,r in enumerate(results):   
        if r not in res_set:     
            annotated_results.append((r, False, "", r))
            res_set.add(r)
        
    return (annotated_results, len(results), None)
