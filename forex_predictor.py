'''
Created on Mar 23, 2015

@author: aelsalla
'''
from DatasetBuilder.DatasetBuilder import DatasetBuilder
from FeaturesExtractor.FeaturesExtractor import FeaturesExtractor
from Classifier.Classifier import Classifier
import matplotlib.pyplot as plt
import numpy as np

# Initialize the DatasetBuilder
###############################
dataSetBuilder = DatasetBuilder()
testSetShare = 0.1
trainSet, testSet = dataSetBuilder.BuildDataSet(testSetShare)

dataSet = []
dataSet.extend(trainSet)
dataSet.extend(testSet)

'''
fullPrices = []
for price in dataSetBuilder.get_prices():
    fullPrices.append(float(price['value']))
'''

fullPrices = []
labels = []
sizes = []
x = []
i = 0
up = 0
down = 0 
for point in dataSetBuilder.full_set:
    x.append(i)
    i = i + 1
    fullPrices.append(point['price'])
    if(point['signal'] == 'Up'):
        labels.append('b')
        sizes.append(np.pi*50)
        up = up + 1  
    elif(point['signal'] == 'Down'):
        labels.append('r')
        sizes.append(np.pi*50)
        down = down + 1
    else:
        labels.append('g')
        sizes.append(np.pi*5)

# Dataset prices and text
prices = []
headlines = []
for item in dataSet:
    prices.append(float(item['price']))
    headlines.append(item['headline'])
    
#plt.plot(fullPrices)
plt.scatter(x, fullPrices, s = sizes, c = labels, marker = 'o')

#plt.plot([1,2,3,4])
plt.show()
#plt.savefig('C:\\Users\\ASALLAB\\Google Drive\\Guru_Forex\\Code\\forex\\plot1.png')
# Initialize FeaturesExtractor
##############################
featuresExtractor = FeaturesExtractor()

# This part is needed to form BoW and score each sentence against it 
'''
fullDataSet = []
fullDataSet.extend(trainSet)
fullDataSet.extend(testSet)
bow = featuresExtractor.ConstructBowWithSentiWordNet(fullDataSet)
trainFeatures, trainLabels = featuresExtractor.ExtractBoWSentiWordNetFeatures(trainSet, bow)
testFeatures, testLabels = featuresExtractor.ExtractBoWSentiWordNetFeatures(testSet, bow)
'''

# This part is needed to get the collective sentiment per sentence by summing up the 3 scores
# It doesn't require a BoW
trainFeatures, trainLabels = featuresExtractor.ExtractCollectiveLexiconSentimentFeatures(trainSet)
testFeatures, testLabels = featuresExtractor.ExtractCollectiveLexiconSentimentFeatures(testSet)


# Initialize Classifier
#######################
classifier = Classifier()

# This part is for lexicon classifier. No training required
print('Training accuracy = ' + str(classifier.LexiconTest(trainFeatures, trainLabels)))
print('Test accuracy = ' + str(classifier.LexiconTest(testFeatures, testLabels)))