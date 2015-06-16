'''
Created on Mar 23, 2015

@author: aelsalla
'''

from FeaturesExtractor.FeaturesExtractor import FeaturesExtractor
#from Classifier.Classifier import Classifier
import sys

labelsMap = {1: 'Positive' , 2: 'Negative'}

def LexiconClassify(features):
    
    if (features[0][0] > features[0][1] or features[0][0] == features[0][1]):
        #pos_score > neg_score
        # Up
        label = 1
    else:
        # Down
        label = 2
        

    
    # Score the final accuracy
    return label

input_text = sys.argv[1]
#input_text = "Hello"

# Initialize FeaturesExtractor
##############################
featuresExtractor = FeaturesExtractor()

# This part is needed to form BoW and score each sentence against it 


# This part is needed to get the collective sentiment per sentence by summing up the 3 scores
# It doesn't require a BoW
item = {}
item['headline'] = input_text
item['signal'] = 'Neutral'
testSet = []
testSet.append(item)
testFeatures, testLabels = featuresExtractor.ExtractCollectiveLexiconSentimentFeatures(testSet)


# Initialize Classifier
#######################
#classifier = Classifier()

# This part is for lexicon classifier. No training required

#print('Lexicon prediction is: ' + str(classifier.LexiconClassify(testFeatures)))
#print('Lexicon prediction is: ' + str(LexiconClassify(testFeatures)))
#print('Lexicon prediction is: ' + labelsMap[LexiconClassify(testFeatures)])
print(labelsMap[LexiconClassify(testFeatures)])




