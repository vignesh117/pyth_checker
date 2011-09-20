#from offset_dict import *
#from nltk.corpus import *

def concord( dic , tokens,word ):
	contexts = []
	#off_dict = offset_dict(tokens)
	offsets  = dic[word]
	contl = []
	contr = []
	
	for i in offsets:
		contl+=[tokens[j] for j in range((i-4),i) if j >=0]
		contr+=[tokens[j] for j in range((i+1),(i+4)) if j<len(tokens)]
       
	"""		
	for i in offsets:
		try:
			contexts+=[tokens[i-5]]
			contexts+=[tokens[i-4]]
			contexts+=[tokens[i-3]]
			contexts+=[tokens[i-2]]
			contexts+=[tokens[i-1]]
			contexts+=[tokens[i+1]]
			contexts+=[tokens[i+2]]
			contexts+=[tokens[i+3]]
			contexts+=[tokens[i+4]]
#			contexts+=[tokens[i+5]]
			
		except IndexError:
			pass
	"""
	#return contexts
	
	return contl + contr
		 


