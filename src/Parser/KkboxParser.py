import requests
import re

from bs4 import BeautifulSoup

from AbstractParser import AbstractParser

class KkboxParser(AbstractParser):

	def __init__(self):
		self.base_url = "http://www.kkbox.com/tw"
		self.search_url = self.base_url + "/tc/search.php?search=lyrics&word="

	def search_by_keywords(self, keywords):
		search_string = '+'.join(keywords)
		url = self.search_url + search_string
		request_text = requests.get(url).text
		soup = BeautifulSoup(request_text, "html.parser")
		lyrics = self.parse_soup(soup)
		sentences = self.parse_lyrics(lyrics)
		return sentences

	def parse_soup(self, soup):
		li_songs = (
			soup
			.findAll('div', {'class': 'container'})[1]
			.findAll('div', {'class': 'row'})[1]
			.find('ul', {'class': 'lyrics'})
			.findAll('li')
		)
		return li_songs[0].find('div', {'class': 'full-lyrics'})
		# print li_songs[0].find('div', {'class': 'full-lyrics'})
		# self.parse_lyrics(li_songs[0].find('div', {'class': 'full-lyrics'}))

	def parse_lyrics(self, lyrics):
		raw_data = re.sub("&amp;|quot;", "", str(lyrics.extract()))
		lyric = raw_data.split('<br>')[-1]
		sentences = lyric.split('<br/>')[:-1]
		sentences = [sentence.strip() for sentence in sentences]
		scores = [len(re.findall("<.*?>", sentence)) for sentence in sentences]
		sentences = [re.sub("<.*?>", "", sentence).rstrip() for sentence in sentences]
		return zip(sentences, scores)
		#for sentence in sentences:
		#	print sentence.strip()

