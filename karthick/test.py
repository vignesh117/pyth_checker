import pickle, os.path
import re, collections
from nltk.metrics import distance

def words(text): return re.findall('[a-z]+', text.lower()) 

def train():
    features=words(file('big.txt').read())
    if os.path.isfile('dictfile')==True:
        model=pickle.load(open('dictfile'))
    else:
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        dfile=open('dictfile','w')
        pickle.dump(dict(model), dfile)
    return model

alphabet = 'abcdefghijklmnopqrstuvwxyz'
NWORDS = train()

def edits1(word):
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b     for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_editsn(word, n):
    edits=set([word])
    for i in range(0,n):
        temp=set()
        for x in edits:
            temp.update(edits1(x))
        edits.update(temp)
    #filter below with diction
    return set(e for e in edits if e in NWORDS)

def wordize(filename):
    f=file(filename).read().lower()
    return re.findall('[a-z]+',f)

def setting():
    w1, w2 = 'markets','capital'
    words=wordize('big.txt')
    trigrams=zip(words,words[1:],words[2:])
    trigrams=[set(x) for x in trigrams]
    print "prep done"
    for x in trigrams:
        if w1 in x and w2 in x:
            print x

def ranked_suggestions(w):
    suggestions=known_editsn(w,2)
    #primary and secondary candidates for correction
    p_cand= []
    s_cand= []
    for s in suggestions:
        d= distance.edit_distance(w,s)
        if d==1:
            p_cand.append(s)
        elif d==2:
            s_cand.append(s)
    p_cand= sorted(p_cand, key=NWORDS.__getitem__)
    s_cand= sorted(s_cand, key=NWORDS.__getitem__)
    return (p_cand+s_cand)[:5]

def driver():
    c=['belive','bouyant','comitte','distarct','extacy','failer','hellpp','gracefull','liason','ocassion','possable','thruout','volly','tatoos','respet']
    for w in c:
        print w, ranked_suggestions(w)

driver()
