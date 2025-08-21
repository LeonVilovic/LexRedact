from collections import defaultdict
#from fuzzywuzzy import fuzz
from rapidfuzz import fuzz


def group_entities_fuzz_logic(entities, threshold=85):
    """
    Args:
        entities (list[dict]): list of entities, each dict must have key 'text'
        threshold (int): fuzzy similarity threshold (0–100)
    """
    clusters = defaultdict(list)

    def normalize(name):
        return name.lower().strip()

    def is_similar(a, b):
        return fuzz.ratio(a, b) >= threshold

    for ent in entities:
        name = ent["text"]
        added = False
        for key in list(clusters.keys()):
            if is_similar(normalize(name), key):
                clusters[key].append(ent)
                added = True
                break
        if not added:
            clusters[normalize(name)].append(ent)

    return dict(clusters)


