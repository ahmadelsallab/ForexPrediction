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
colors = []
time_stamps = []
x = []
i = 0
up = 0
down = 0 
for point in reversed(dataSetBuilder.full_set):
    x.append(i)
    i = i + 1
    fullPrices.append(point['price'])
    if(point['signal'] == 'Up'):
        colors.append('b')
        #sizes.append(np.pi*50)
        sizes.append(np.pi*0)
        labels.append('+')
        up = up + 1
        time_stamps.append(point['time_stamp'])  
    elif(point['signal'] == 'Down'):
        colors.append('r')
        #sizes.append(np.pi*50)
        sizes.append(np.pi*0)
        labels.append('-')
        down = down + 1
        time_stamps.append(point['time_stamp'])
    else:
        colors.append('g')
        #sizes.append(np.pi*5)
        sizes.append(np.pi*0)
        labels.append('.')
        time_stamps.append('.')

# Dataset prices and text
prices = []
headlines = []
for item in reversed(dataSet):
    prices.append(float(item['price']))
    headlines.append(item['headline'])
    
#plt.plot(fullPrices)
y = fullPrices
plt.scatter(x, y, s = sizes, c = colors, marker = '.')

for label, x, y in zip(labels, x, y):
    plt.annotate(label, xy = (x, y))

#plt.plot([1,2,3,4])
plt.xlabel('Time stamp')
plt.ylabel('Price stamp')
plt.title('Prices vs. sentiment')
plt.axes()
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

'''
# This part is needed to get the collective sentiment per sentence by summing up the 3 scores
# It doesn't require a BoW
trainFeatures, trainLabels = featuresExtractor.ExtractCollectiveLexiconSentimentFeatures(trainSet)
testFeatures, testLabels = featuresExtractor.ExtractCollectiveLexiconSentimentFeatures(testSet)
'''
# This part is extracting the BoW features scoring for the 3 scores per each word
BoW = featuresExtractor.ConstructBowWithSentiWordNet(dataSet)
trainFeatures, trainLabels = featuresExtractor.ExtractBoWSentiWordNetFeatures(trainSet, BoW)
testFeatures, testLabels = featuresExtractor.ExtractBoWSentiWordNetFeatures(testSet, BoW)

# Initialize Classifier
#######################
classifier = Classifier()

# This part is for lexicon classifier. No training required
'''
print('Training accuracy = ' + str(classifier.LexiconTest(trainFeatures, trainLabels)))
print('Test accuracy = ' + str(classifier.LexiconTest(testFeatures, testLabels)))
'''

train_err = classifier.NNTrain(trainFeatures, trainLabels, plot=True)
test_err = classifier.NNTest(testFeatures, testLabels,  plot=True)
print('Training accuracy = ' + str((len(trainFeatures) - train_err) / len(trainFeatures)))
print('Test accuracy = ' + str((len(testFeatures) - test_err) / len(testFeatures)))