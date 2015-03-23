'''
Created on Mar 23, 2015

@author: aelsalla
'''
from DatasetBuilder.DatasetBuilder import DatasetBuilder
from FeaturesExtractor.FeaturesExtractor import FeaturesExtractor
from Classifier.Classifier import Classifier

# Initialize the DatasetBuilder
###############################
dataSetBuilder = DatasetBuilder()
testSetShare = 0.1
trainSet, testSet = dataSetBuilder.BuildDataSet(testSetShare)


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
print('Training accuracy = ' + classifier.LexiconTest(trainFeatures, trainLabels))
print('Test accuracy = ' + classifier.LexiconTest(testFeatures, testLabels))