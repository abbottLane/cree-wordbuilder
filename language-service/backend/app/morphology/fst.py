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

        print("QUERY: " + query_text)

        start = time.time()
        results = completions.apply_down(query_text)
        end = time.time()

        print("RESULTS: (" + str(end-start) + ") " + str(results))
    return results

# async def is_complete_form(seq):
#     result = list(fst.apply_down(re.sub("-", "", seq))) # remove morph bounds before verifying word
#     if len(result) > 0:
#         return True
#     return False

# async def process_fst_query(query_text):
#     if query_text:
#         results = fst.apply_down(query_text.split()[0]) # assumes an inverted hfst model (suffixed w/ .i)
#         segmented_results = segmenter.apply_down(query_text, debug=False)
       
#         parsed_results = []
#         for r in list(results):
#             parsed_results.append(parse_result(r, query_text, segmented_results))

#         for pr in parsed_results:
#             # enrich with dictionary information
#             pr["dict_entries"] = entries_by_root(pr["root"])
#             # enrich with surface form
#             pr["surface_form"] = query_text

#     return parsed_results
   
# def parse_result(result, query, segmented_results):
#     # Process Verb analyses
#     if "[V]" in result: 
#         return process_verb_analysis(result, segmented_results)

#     # process Noun analyses
#     elif "Noun" in result: 
#         return process_noun_analysis(result, query, segmented_results)

#     else:
#         return process_other_analysis(result, query, segmented_results)

# def process_other_analysis(analysis, query, segmented_results):
#     return {
#         "root": query, 
#         "affixes": [analysis.lstrip('[').rstrip(']')], 
#         "analyzed_form":analysis, 
#         "pos": "Other",
#         "morphs": analyzed2english(analysis,  segmented_results)
#     }

# def process_noun_analysis(noun_analysis, noun_form, segmented_results):
#     return {
#         "root": noun_form, 
#         "affixes": [noun_analysis.lstrip('[').rstrip(']')], 
#         "analyzed_form":noun_analysis, 
#         "pos": "Noun",
#         "morphs": analyzed2english(noun_analysis,  segmented_results)
#     }

# def process_verb_analysis(verb_analysis, segmented_results):
#     root = get_stem(verb_analysis)
#     affixes=[]
#     for affix_str in verb_analysis.split(root):
#         tags = get_tags(affix_str)
#         for t in tags:
#             affixes.append(t)
    
#     ret =  {
#         "root": root, 
#         "affixes": affixes, 
#         "analyzed_form":verb_analysis, 
#         "pos":"Verb",
#         "morphs": analyzed2english(verb_analysis, segmented_results)
#     }
#     return ret

# def get_stem(verb):
#     return re.sub('\[.*?\]', "", verb)

# def get_tags(affix_str):    
#     return [x.rstrip(']').lstrip('[') for x in re.findall("\[.*?\]", affix_str)]

# def analyzed2english(analyzed_form, segmented_results):
#     inside_tag = False
#     tags = []
#     current_tag = ""
#     for tok in analyzed_form:
#         if tok == "]" or tok == "[":
#             if tok == "[":
#                 if current_tag:
#                     tags.append(current_tag)
#                     current_tag = ""
#                 inside_tag == True
#             elif tok == "]":
#                 tags.append(current_tag)
#                 current_tag = ""
#                 inside_tag == False
#         else:
#             current_tag += tok
#     tags = ["["+t+"]" for t in tags if t not in {"V", "N"}]
#     print("tags:" + str([t for t in tags]))
#     print("segmented:" + str([t for t in segmented_results]))
#     tags = pair_segmentation(tags, segmented_results)
#     return [{"tag":t[0], "surface":t[1], "en": TAG2ENG_MAP[t[0]] if t[0] in TAG2ENG_MAP else "ROOT"} for t in tags]

# def pair_segmentation(tags, segmentations):
#     len_tags = len(tags)
#     segmentations = [s.rstrip("^").split("^") for s in segmentations]
#     for s in segmentations:
#         if len(s) == len_tags:
#             return zip(tags,s)
#     else:
#         return zip(tags, segmentations[0]) # just return first analysis if lengths dont match

