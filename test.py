'''
import urllib
from bs4 import BeautifulSoup
url = 'https://in.finance.yahoo.com/q/h?s=EURUSD%3DX&t=2015-01-26'
data = urllib.request.urlopen(url)
soup = BeautifulSoup(data)

divs = soup.find('div',attrs={'id':'yfi_headlines'})
div = divs.find('div',attrs={'class':'bd'})
ul = div.find('ul')
lis = ul.findAll('li')
hls = []
for li in lis:
    headlines = li.find('a').contents[0]
    print(headlines)
'''

from FeaturesExtractor.sentiwordnet import SentiWordNetCorpusReader, SentiSynset
#from nltk.corpus.reader.sentiwordnet import SentiWordNetCorpusReader, SentiSynset


swn_filename = '.\\Classifier\\input\\SentiWordNet_3.0.0_20130122.txt'
swn = SentiWordNetCorpusReader(swn_filename)
syn = swn.senti_synset('breakdown.n.03')
#syn = swn.senti_synset('euro')
print(syn.pos_score)
print(syn.neg_score)
print(syn.obj_score)
synsets = swn.senti_synsets('slow')

'''
for synset in synsets:
    #print(synset._name)
    print(synset)
'''

'''
from DatasetBuilder.DatasetBuilder import DatasetBuilder

d = DatasetBuilder()
'''
#d.parse_news_url('DatasetBuilder\\input\\view-source feeds.marketwatch.com marketwatch realtimeheadlines_20_3_2015.html')
#d.parse_news_url('http://feeds.marketwatch.com/marketwatch/realtimeheadlines/')

'''
import urllib.request
from bs4 import BeautifulSoup

#f = open('DatasetBuilder\\input\\view-source feeds.marketwatch.com marketwatch realtimeheadlines_20_3_2015.html', 'r')
#f = open('DatasetBuilder\\input\\view-source feeds.marketwatch.com marketwatch realtimeheadlines_22_3_2015.html', 'r')
#f = urllib.request.urlopen('http://feeds.marketwatch.com/marketwatch/realtimeheadlines/')

#f = open('http://feeds.marketwatch.com/marketwatch/realtimeheadlines/', 'r')


#f = urllib.request.urlopen('http://feeds.marketwatch.com/marketwatch/realtimeheadlines?format=html')
f = urllib.request.urlopen('http://feeds.marketwatch.com/marketwatch/realtimeheadlines?format=xml')


soup = BeautifulSoup(f.read())  

for b in soup.findAll('li', { "class" : "regularitem" }):
    print(b.findAll('h4', { "class" : "itemtitle" })[0].text.strip())
    print(b.findAll('h5', { "class" : "itemposttime" })[0].text.strip())
    #print(b.findAll('span'))

'''

'''
from xml.dom import minidom
import urllib.request
import calendar

f = urllib.request.urlopen('http://feeds.marketwatch.com/marketwatch/realtimeheadlines?format=xml')
xmldoc = minidom.parse(f)    

# Get the user share balance option
items = xmldoc.getElementsByTagName('item')

for item in items:
    print(item.getElementsByTagName('title')[0].firstChild.data)
    print(item.getElementsByTagName('pubDate')[0].firstChild.data)
    #Sat, 21 Mar 2015 17:46:14 GMT
    datetime = item.getElementsByTagName('pubDate')[0].firstChild.data
    removed_day_name = datetime.split(',')[1]
    day = removed_day_name.split(' ')[1]
    month_name = removed_day_name.split(' ')[2]
    month = str(list(calendar.month_abbr).index(month_name)).zfill(2)
    year = removed_day_name.split(' ')[3]
    hour_min_sec =  removed_day_name.split(' ')[4]
    hour = hour_min_sec.split(':')[0]
    min = hour_min_sec.split(':')[1]
    sec = hour_min_sec.split(':')[2]
    
    print(year + month + day + ' ' + hour + min + sec)
    
'''


'''
from DatasetBuilder.DatasetBuilder import DatasetBuilder

d = DatasetBuilder()
news_headlines = d.ParseNewsURL('http://feeds.marketwatch.com/marketwatch/realtimeheadlines?format=xml')

for headline in news_headlines:
    print(headline['text'] + '\n' + headline['time_stamp'])
d.DumpNewsCSV(news_headlines)
'''