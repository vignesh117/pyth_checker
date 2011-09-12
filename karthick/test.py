import pickle, os.path
import re, collections

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
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
NWORDS = train(words(file('big.txt').read()))

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

def driver():
    print known_editsn("corect",2)
    print edits1('acress')
    print NWORDS['correct']

driver()
