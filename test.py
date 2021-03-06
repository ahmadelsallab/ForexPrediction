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
'''
from FeaturesExtractor.sentiwordnet import SentiWordNetCorpusReader, SentiSynset
#from nltk.corpus.reader.sentiwordnet import SentiWordNetCorpusReader, SentiSynset


swn_filename = '.\\FeaturesExtractor\\input\\SentiWordNet_3.0.0_20130122.txt'
swn = SentiWordNetCorpusReader(swn_filename)
#syn = swn.senti_synset('breakdown.n.03')
syn = swn.senti_synsets('slow')[0]
#syn = swn.senti_synset('euro')
print(syn.pos_score)
print(syn.neg_score)
print(syn.obj_score)
synsets = swn.senti_synsets('slow')
'''

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

'''
import urllib.request
from bs4 import BeautifulSoup
import json
f = urllib.request.urlopen('http://www.myfxbook.com/getHistoricalDataByDate.json?&start=2015-03-01%2000:00&end=2015-03-24%2000:00&symbol=EURUSD&timeScale=60&userTimeFormat=0&rand=0.5403805375099182')
#f = open('C:\\Users\\ASALLAB\\Google Drive\\Guru_Forex\\Code\\forex\\DatasetBuilder\\input\\EURUSD Euro vs US Dollar EUR USD Historical Forex Data   Myfxbook.html', 'r', encoding = 'utf-8')
'''

'''
soup = BeautifulSoup(f.read())  

#for b in soup.findAll('span', { "name" : "timeEURUSD" }):
for b in soup.findAll('tr', { "onmouseover" : "this.className='normalActive';" }):
    #print(b.text.strip())
    print(b.findAll('span', { "name" : "timeEURUSD" })[0].text.strip())
    print(b.findAll('span', { "name" : "closeEURUSD" })[0].text.strip())
    #print(b.findAll('h5', { "class" : "itemposttime" })[0].text.strip())
    #print(b.findAll('span'))
'''
'''
json_data = json.loads(f.read().decode('utf8'))
#json_data = json.loads(f)
#print(json_data)
soup = BeautifulSoup(json_data['content']['historyData'])  

#for b in soup.findAll('span', { "name" : "timeEURUSD" }):
for b in soup.findAll('tr', { "onmouseover" : "this.className='normalActive';" }):
    #print(b.text.strip())
    print(b.findAll('span', { "name" : "timeEURUSD" })[0].text.strip())
    print(b.findAll('span', { "name" : "closeEURUSD" })[0].text.strip())
    #print(b.findAll('h5', { "class" : "itemposttime" })[0].text.strip())
    #print(b.findAll('span'))
'''
'''
from DatasetBuilder.DatasetBuilder import DatasetBuilder

d = DatasetBuilder()
prices = d.ParsePricesURL()

for price in prices:
    print(price['value'] + '\n' + price['time_stamp'])
d.DumpPricesCSV(prices)

'''
'''
import numpy as np
import neurolab as nl
# Create train samples
input = np.random.uniform(-0.5, 0.5, (10, 2))
target = (input[:, 0] + input[:, 1]).reshape(10, 1)
# Create network with 2 inputs, 5 neurons in input layer and 1 in output layer
net = nl.net.newff([[-0.5, 0.5], [-0.5, 0.5]], [5, 1])
# Train process
err = net.train(input, target, show=15)
# Test
net.sim([[0.2, 0.1]]) # 0.2 + 0.1
print(net.sim([[0.2, 0.1]]))
'''
'''
from DatasetBuilder.DatasetBuilder import DatasetBuilder
import matplotlib.pyplot as plt
import numpy as np

#plt.plot([1,2,3,4], ['+','-','+','+'])
#plt.scatter([1,2,3,4], [1,2,3,4], s= [0, np.pi*10, 0, np.pi*100], c = ['g', 'g', 'b', 'b'], marker = '+')
plt.scatter([1,2,3,4], [1,2,3,4], s= [0, np.pi*0, 0, np.pi*0], c = ['g', 'g', 'b', 'b'], marker = '+')
labels = ['+','-','+','+']
x = [1,2,3,4]
y = [1,2,3,4]
for label, x, y in zip(labels, x, y):
    plt.annotate(label, xy = (x, y))
    
plt.ylabel('some numbers')
plt.show() # If you show the image is not saved to the file
#plt.savefig('C:\\Users\\ASALLAB\\Google Drive\\Guru_Forex\\Code\\forex\\plot.png')
'''
'''
# Different markers scatter:
cond = df.col3 > 300
subset_a = df[cond].dropna()
subset_b = df[~cond].dropna()
plt.scatter(subset_a.col1, subset_a.col2, s=120, c='b', label='col3 > 300')
plt.scatter(subset_b.col1, subset_b.col2, s=60, c='r', label='col3 <= 300') 
plt.legend()
'''

'''
import numpy as np
import neurolab as nl
# Create train samples
input = np.random.uniform(-0.5, 0.5, (10, 2))
target = (input[:, 0] + input[:, 1]).reshape(10, 1)
# Create network with 2 inputs, 5 neurons in input layer and 1 in output layer
net = nl.net.newff([[-0.5, 0.5], [-0.5, 0.5]], [5, 1])
# Train process
err = net.train(input, target, show=15)
# Test
net.sim([[0.2, 0.1]]) # 0.2 + 0.1
print(net.sim([[0.2, 0.1]]))

'''

'''
import threading, time, datetime
now = datetime.datetime.now()
open_time = datetime.datetime(now.year, now.month, now.day, 18,38,0);
close_time = datetime.datetime(now.year, now.month, now.day, 18,39,0); 

def isAlarmExpired(time):
        
    if((time >= open_time.time())  & (time <= close_time.time())):
        return True
    else:
        return False
    
def crawl():
    print('Crawling now ' + str(datetime.datetime.now()))
while True:
    if(isAlarmExpired(datetime.datetime.now().time())):
        d = threading.Thread(target=crawl)
        d.start()
'''

'''
# ROC
#----
import numpy as np
import pylab as pl
from sklearn import svm, datasets
from sklearn.utils import shuffle
from sklearn.metrics import roc_curve, auc

random_state = np.random.RandomState(0)

# Import some data to play with
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Make it a binary classification problem by removing the third class
X, y = X[y != 2], y[y != 2]
n_samples, n_features = X.shape

# Add noisy features to make the problem harder
X = np.c_[X, random_state.randn(n_samples, 200 * n_features)]

# shuffle and split training and test sets
X, y = shuffle(X, y, random_state=random_state)
half = int(n_samples / 2)
X_train, X_test = X[:half], X[half:]
y_train, y_test = y[:half], y[half:]

# Run classifier
classifier = svm.SVC(kernel='linear', probability=True)
probas_ = classifier.fit(X_train, y_train).predict_proba(X_test)

# Compute ROC curve and area the curve
fpr, tpr, thresholds = roc_curve(y_test, probas_[:, 1])
roc_auc = auc(fpr, tpr)
print ("Area under the ROC curve : %f" % roc_auc)

# Plot ROC curve
pl.clf()
pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
pl.plot([0, 1], [0, 1], 'k--')
pl.xlim([0.0, 1.0])
pl.ylim([0.0, 1.0])
pl.xlabel('False Positive Rate')
pl.ylabel('True Positive Rate')
pl.title('Receiver operating characteristic example')
pl.legend(loc="lower right")
pl.show()
'''

# Precision-Recall:
#------------------
import numpy as np
import pylab as pl
from sklearn import svm, datasets
from sklearn.utils import shuffle
from sklearn.metrics import precision_recall_curve, auc

random_state = np.random.RandomState(0)

# Import some data to play with
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Make it a binary classification problem by removing the third class
X, y = X[y != 2], y[y != 2]
n_samples, n_features = X.shape

# Add noisy features to make the problem harder
X = np.c_[X, random_state.randn(n_samples, 200 * n_features)]

# shuffle and split training and test sets
X, y = shuffle(X, y, random_state=random_state)
half = int(n_samples / 2)
X_train, X_test = X[:half], X[half:]
y_train, y_test = y[:half], y[half:]

# Run classifier
classifier = svm.SVC(kernel='linear', probability=True)
probas_ = classifier.fit(X_train, y_train).predict_proba(X_test)

# Compute Precision recall curve and area the curve
precision, recall, thresholds = precision_recall_curve(y_test, probas_[:, 1])
area = auc(recall, precision)
print ("Area under the ROC curve : %f" % area)

# Plot Precision recall curve
pl.clf()
pl.plot(recall, precision, label='Precision-Recall curve')
pl.xlabel('Recall')
pl.ylabel('Precision')
pl.ylim([0.0, 1.05])
pl.xlim([0.0, 1.0])
pl.title('Precision-Recall example: AUC=%0.2f' % area)
pl.legend(loc="lower left")
pl.show()