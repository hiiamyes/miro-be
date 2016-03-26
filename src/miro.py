from pyquery import PyQuery as pq
import random

#encoding=utf-8
import jieba
import jieba.analyse
jieba.set_dictionary('asset/dict.txt.big')

def getTag(sentence):
    tags = jieba.analyse.extract_tags(sentence)
    return tags[0]

def getSong(word):
    d = pq('http://www.kkbox.com/tw/tc/search.php?search=lyrics&word=' + word)
    n = d('ul.lyrics li').length
    r = random.randint(0, n-1)

    # get name of song
    name = d('ul.lyrics li:nth-child(' + str(r) + ') h4 a:first').text()

    # get partial lyrics of song
    lyricsFull = d('.full-lyrics').eq(r).text().split(' ')
    lyricPartialIndex = 0;
    for index, lyric in enumerate(lyricsFull):
        if lyric == word:
            lyricPartialIndex = index;
            break;
    lyricPartial = lyricsFull[lyricPartialIndex-1] + '，' + lyricsFull[lyricPartialIndex] + '，' + lyricsFull[lyricPartialIndex+1] + '。';

    return {'name': name, 'lyric_partial': lyricPartial}

def getLink(song):
    d = pq('http://www.youtube.com/results?search_query=' + song)
    links = d('a.yt-uix-sessionlink.yt-uix-tile-link.spf-link.yt-ui-ellipsis.yt-ui-ellipsis-2')
    i = 0
    while pq(links[i]).attr('href').index('/watch') != 0:
        i+=1
    title = pq(links[i]).attr('title')
    link = 'http://www.youtube.com' + pq(links[i]).attr('href');
    return link

def Miro(sentence):
    if sentence != '':
        tag = getTag(sentence)
        song = getSong(tag)
        link = getLink(song['name'])

    song['link'] = link

    return (song)
