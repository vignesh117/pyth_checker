from nltk.probability import GoodTuringProbDist
from nltk.corpus import *
from nltk import *
import os, re
import  edit_distances,  find_context



def train(tests):
	#files = os.listdir(c_dir)
	#print files
	#for f in files:
	c_dir = "/home/such/Documents/NLP/Programming_Assignment_resources/"
	fpath = c_dir+'big.txt'
	doc = open(fpath,'r')
	words = re.findall('[a-z]+' , doc.read().lower())
	
	#define n-gram model
	#corp = brown.words()
	good_turing = lambda fdist,bins:GoodTuringProbDist(fdist,56707)
	model = NgramModel(3,words,good_turing)
	
	
	for s in tests:
		# Finding the possible misspelled words
		misspelled = []
		sentences = s.split('.')
		for sentence in sentences:
			word = sentence.split(' ')
			for w in word:
				if w.lower() not in words and w.lower() != '':
					misspelled.append(w)
	
	
		#finding the candidate words for words in the misspelled array
		candidates = {}
		for wrong in misspelled:
			pos = s.index(wrong)
			candidates[wrong] = (list(edit_distances.correct(wrong)))
		#print misspelled
		#print candidates
	
		
		# Find the n-gram probabilities for each correction
		corrections = {} # the dictionar which keeps the MLE for each correction for all misspelled
		for k in candidates.keys():
			MLEs = []
			for cand in candidates[k]:
				estimates = find_context.find_contexts(cand, s, model)
				MLEs.append((cand,estimates))
				#print MLEs
			corrections[k] = MLEs
	
		#Suggest the corrections
		m = lambda x: max(x,key = lambda y:y[1])
		for k in corrections.keys():		
			final_list = [c for c in corrections[k] if c[1] >0 and c[1] <=1]
			print "misspelled :" + k +"\n"
			print "correction :"  + m(final_list)[0] + str(m(final_list)[1])+ "\n\n"
	
	

def test():
	test_data = ['Securities and Echane Commission','international capitan markets','educational nsitutions',
	'mewn and women','United tates','The impending takeover bid increased the stock value of the bak.',
	'The fugitive oldiers from the military were finally arrested today.','The fisherman went fishing close to the river bak.',
	'All divisions of the ramed forces participated in the parade.','The departments of the institute offer corses, conducted by highly qualified staff.']
	train(test_data)
test()
