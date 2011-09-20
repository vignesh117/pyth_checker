
#changing the way we compute the concordance

from nltk.probability import *
from nltk.corpus import *
from nltk import *
from collections import *
from context_words import *
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from similarity import *
import os, re
import  edit_distances,  find_context


#gives the indices of  all words
def offset_dict(words):
	offsets = defaultdict(list)
	enum_words = enumerate(words)
	for index,word in enum_words:
		offsets[word].append(index)
	return offsets
	

def train(tests):

	#files = os.listdir(c_dir)
	#print files
	#for f in files:
	c_dir = "/home/such/Documents/NLP/Programming_Assignment_resources/"
	fpath = c_dir+'big.txt'
        #stemmer  = WordNetStemmer()
        #stem = lambda x:stemmer.stem(x)
	
	stops = stopwords.words('english')
	doc = open(fpath,'r')
	words = re.findall('[a-z]+' , doc.read().lower())	
	#words2 = [ w for w in words if w not in stops]
	#define n-gram model from the file stored using pickel
	
	#corp = pickle.load(open('corpfile'))
	corp = map(lambda x :x.lower(), brown.words()) 
	ispresent = lambda x : wn.words(x) != []
	#corp = filter(ispresent, corp)
	#corp_words = re.findall('[a-z]+' , corp)
	#corp = [ w for w in corp if w not in stops]
	corp_dict = offset_dict(corp)
	for s in tests:
		print s
		test_words = re.findall('[a-z]+' , s.lower())
		# Finding the possible misspelled words
		misspelled = []
		sentences = s.split('.')
		#mispos = {}
		#sentences = [s for s in sentences if s not in stops]
		for t_word in test_words :
                    if t_word.lower() not in words and t_word.lower() != '':
					misspelled.append(t_word.lower())
					#mispos[w.lower()] = s.index(w)
		#print mispos
			
		#finding the candidate words for words in the misspelled array
		candidates = {}
		for wrong in misspelled:
			#pos = s.index(wrong)
			candidates[wrong] = (list(edit_distances.correct(wrong)))
				
		#find the context words for the test sentences and the corpus
		corrections = {}
                for miss in misspelled:
			print test_words
			#find the context words for the mispelled words
			error_dict = offset_dict(test_words)
			error_context = list(set(concord(error_dict,test_words,miss)))
			error_context = [e for e in error_context if e not in stops]
			errcont = []
			for errc in error_context:
				errcont += list(set(concord(corp_dict,corp,errc)))
			errcont = filter(ispresent,errcont)
			errcont = [e for e in errcont if e not in stops]
                        errcont += error_context
			#
			#print "error context"
			#print error_context

			#print errcont
			#for each context word find how often they co-occur with each of the corrections
			counts = {}
			can_list = candidates[miss]
			#print can_list
			for c in can_list:
				cand_cooccur = list(set(concord(corp_dict,corp,c)))   #change the corpus here
				#cand_cooccur = filter(lambda x: edit_dist(c,miss) < 2, cand_cooccur)
				cand_cooccur = filter(ispresent,cand_cooccur)
				cand_cooccur = [ca for ca in cand_cooccur if ca not in stops]
				#print "printing candidate context for" + c +".....................\n\n\n\n"
				#print "candidate contexts for "+c
				#print cand_cooccur
				count = sum([cand_cooccur.count(i) for i in errcont])
				counts[c] = count,sim(errcont,c)
		
                        print counts
			corrections[miss] = max(counts,key = lambda a:counts.get(a))
			p = test_words.index(miss)
                        test_words[p] = max(counts,key = lambda a:counts.get(a))
                       
	
		#Suggest the corrections
		
			
			print "misspelled :" + miss +"\n"
			try:
				print "correction :"  + corrections[miss] + "\n\n"
			except ValueError:
				pass
		
def test():
	test_data = ['Securities and Echane Commission','international capitan markets','educational nsitutions',
	'mewn and women','United tates','The impending takeover bid increased the stock value of the bak.',
	'The fugitive oldiers from the military were finally arrested today.','The fisherman went fishing close to the river bak.',
	'All divisions of the ramed forces participated in the parade.','The departments of the institute offer corses, conducted by highly qualified staff.']
	
	test_data2 = ['Who said it is difficult, it is impossile', 'The best part of the stiry is yet to come.',
	'Keep your frinds close, and your enemis closer.','The powre has now shifted to the east.',
	'You cannot handel the truth.','A great victry has come but at a great cort.','The crime raet seems to be under control.',
	'To be or to bea is not the question.','All divisions of the ramed forces participated in the parade.',
	'In great powrr lies great responsibility.','The food served in the restarant was very godd.',
	'The fotball match was very interesting.','Private hopitals to provide frea treatment to the poor.',
	'The parliament passed the resoltion to discuss the bil.']
	
	test_data4=['The departmnt is very proactve in setting up the syllabus.The corses can be picked in any combination.You can either credit or adit a particular subject.But the cosent of the teacher is required in either case.']
	
	test_data5 = [' Medical tretment is very expnsive nowadays. The por people cannot manage the huge costs. Something needs to be done to make it affardable.Government needs to stwp up and take chage.']
	train(test_data)
test()
