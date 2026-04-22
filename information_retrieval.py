from collections import Counter
def tfCounter(term: list[str], document: list[list[str]]) :
    for doc in document:
        for t in term:
            freq = Counter(doc)
            return {t: freq.get(t, 0) for t in term}
            

def tfIdfCounter():
    pass

