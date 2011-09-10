from nltk.probability import GoodTuringProbDist
from nltk.corpus import *

from nltk import *
import re
def find_contexts(c,text,model):
	#text = re.findall('[a-z]+',text.lower())
	text = text.split('.')
	text = [t for t in text if t != '']
	text=(' ').join(text)
	print text
	try:
		return model.prob(c,[text])
	except TypeError:
		return 0.0
		
