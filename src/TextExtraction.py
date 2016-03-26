import codecs
import jieba
import jieba.posseg as pseg

def extract(input_string):
	sentences = input_string.split(" ")
	seg_list = [ item for sentence in sentences for item in pseg.lcut(sentence) ]
	for word, flag in seg_list:
		print word, flag
	return [[word,flag] for word,flag in seg_list]

def get_score(seg_list):
	with codecs.open("Uni_TW_CP950", "r", "utf-8") as f:
		dictionary = f.readlines()
		dictionary = map(lambda x: x[:-1], dictionary)
		dictionary = map(lambda x: x.split("\t"), dictionary)
		dictionary = dict((p[0],p[1]) for p in dictionary)
	for word, flag in seg_list:
		print word
		print dictionary.setdefault(word, 0)
	return [ [word, flag, int(dictionary.setdefault(word, 0))] for word, flag in seg_list ]

def select_keywoards(score_list):
	keys = []
	for word, flag, score in score_list:
		keys.append([word, calculate_score(flag, score)])
	keys.sort(key=lambda x: x[1])
	print " / ".join([pair[0] for pair in keys])
	max_count = min(len(keys), 2)
	return [pair[0] for pair in keys][0:max_count]


def calculate_score(flag, score):
	if flag == "ns":
		return score / 1.3
	elif flag == "t":
		return score / 1.2
	elif flag == "n":
		return score / 1.1
	elif flag == "v":
		return score / 1.2
	else:
		return score

def select_sentences(sentences):
	print len(sentences)
	sentences = [[i, pair[0], pair[1]] for (i, pair) in enumerate(sentences)]
	index = max(sentences, key=lambda x:x[2])[0]
	if index + 1 < len(sentences) and sentences[index+1][1] != "":
		return [sentence for (_, sentence, _) in sentences[index:index+2]]
	elif index != 0 and sentences[index-1][1] != "":
		return [sentence for (_, sentence, _) in sentences[index-1:index+1]]
	else:
		return [sentences[index][1]]




