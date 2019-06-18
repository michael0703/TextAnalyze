import json
import jieba

def LoadDict(path):
	file = open(path, 'r') 
	js = file.read()
	dic = json.loads(js)   
	return dic


from collections import Counter
def CalSentiment(sentence, pos_dict, neg_dict, SumofPosdict, SumofNegdict):
	
#     with open('stopwords.txt', 'r') as f:
#         stopwords = [term.replace('\n', '') for term in f.readlines()]
#     print(stopwords)
	seg = jieba.cut(sentence)
#     seg = [word for word in seg if word not in stopwords]
#     print(seg)
	

	
	
	Pos_prob = SumofPosdict / (SumofNegdict + SumofPosdict)
	Neg_prob = SumofNegdict / (SumofPosdict + SumofNegdict)
	
	for word in seg:
		if word in pos_dict.keys():
			Pos_prob *= pos_dict[word] / SumofPosdict
#             print('Pos', word, pos_dict[word], Pos_prob)
		else:
			Pos_prob *= 1 / SumofPosdict
		if word in neg_dict.keys():
			Neg_prob *= neg_dict[word] / SumofNegdict
#             print('Neg', word, neg_dict[word], Neg_prob)
		else:
			Neg_prob *= 1 / SumofNegdict
			
#     Pos_prob /= SumofPosdict
#     Neg_prob /= SumofNegdict
	
	return Pos_prob, Neg_prob
	

# pos_dict = LoadDict(pos_path)
# neg_dict = LoadDict(neg_path)    
# SumofPosdict = sum(Counter(pos_dict).values())
# SumofNegdict = sum(Counter(neg_dict).values())

def CalArticle(article, pos_dict, neg_dict, SumofPosdict, SumofNegdict):
	pos_prob = 1
	neg_prob = 1
	for sentence in article:
		# print(sentence)
		tmp_pos, tmp_neg = CalSentiment(sentence, pos_dict, neg_dict, SumofPosdict, SumofNegdict)
		# print(tmp_pos, tmp_neg)
		try:
			if pos_prob == 0:
				pos_prob = 1
			pos_prob *= ((tmp_pos)/(tmp_pos+tmp_neg))
		except:
			pos_prob = 0
		try:
			if neg_prob == 0:
				neg_prob = 1
			neg_prob *= ((tmp_neg)/(tmp_pos+tmp_neg))
		except:
			neg_prob = 0
			
	try:
		pos = pos_prob / (pos_prob + neg_prob)
	except:
		pos = 0
	try:
		neg = neg_prob / (pos_prob + neg_prob)
	except:
		neg = 0
	
	return pos, neg



