from Parser.KkboxParser import KkboxParser
import TextExtraction as TE

def response_with_lyrics(sentence):
	seg_list = TE.extract(sentence)
	score_list = TE.get_score(seg_list)
	keywords = TE.select_keywoards(score_list)
	parser = KkboxParser()
	sentences = parser.search_by_keywords(keywords)
	results = TE.select_sentences(sentences)
	return " ".join(results)
