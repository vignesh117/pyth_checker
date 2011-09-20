from nltk.corpus import wordnet as wn
from collections import *

#function takes a list of context words of the mispelled word an the candidates(top3) and produces the weighted sum of their similarity with the context words
def syn(conw,candw):
    syn_strings = lambda x : str(x)[8:-2]
    pos = lambda y : y[-4:]
        
    #find the synsets of the context word
    ssets = wn.synsets(conw)
    sset_strings = map(syn_strings,ssets)

    #synsets of the candidate word
    csets = wn.synsets(candw)
    cset_strings = map(syn_strings,csets)

    #take a synset whose part of speech matches
    
    matches = [(i,j) for i in range(len(sset_strings)) for j in range(len(cset_strings)) if pos(sset_strings[i]) == pos(cset_strings[j])]
    similarity = 0
    if matches != []:
          
        (k,l) = matches[0]
        similarity = wn.path_similarity(ssets[k],csets[l])
    else:
        similarity = 0

    if similarity is None:
        return 0
    else:
        return similarity
    
def sim(contexts,candidate):
    can_weight = defaultdict(list)
    cansum = 0
    weights = [syn(candidate,cont) for cont in contexts]
    if weights is not None:
        cansum = sum(weights)

    return cansum


cont = ['credit','subject']
cand = ['audit','admit']

#print sim(cont,'audit')
