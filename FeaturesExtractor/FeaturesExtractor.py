'''
Created on Mar 23, 2015

@author: aelsalla
'''
from FeaturesExtractor.sentiwordnet import SentiWordNetCorpusReader, SentiSynset

class FeaturesExtractor(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        swn_filename = '.\\FeaturesExtractor\\input\\SentiWordNet_3.0.0_20130122.txt'
        self.swn = SentiWordNetCorpusReader(swn_filename)
        
        self.labelsMap = {'Up' : 1, 'Down': 2}
        
    def ConstructBowWithSentiWordNet(self, dataSet):
             
        bow = {}
        # If a word is encountered in the dataset, and has an entry (or a synset) in the Senti WordNet, then add it to the BoW
        for item in dataSet:
            for word in item['headline'].split(' '):
                # Insert new words only
                if word not in bow:
                    try:
                        syn = self.swn.senti_synset(word)

                        bow[word] = {}
                        bow[word]['pos_score'] = syn.pos_score
                        bow[word]['neg_score'] = syn.neg_score
                        bow[word]['obj_score'] = syn.obj_score
                    except:
                        # No entry in Senti WordNet
                        continue
                      
                    
                    
                
        return bow  
    # Each entry has numBowEntries * 3, for each word we have 3 scores: +/-/obj if the word exists in the sentence, else 0,0,0
    def ExtractBoWSentiWordNetFeatures(self, dataSet, bow):
        
        # Initialize the features and labels
        features = []
        labels = []
        
        # Score the features against the dataset
        for item in dataSet:
            feature = []
            for senti_word in bow:                
                if senti_word in item['headline'].split(' '):
                    feature.extend([senti_word['pos_score'], senti_word['neg_score'], senti_word['obj_score']])
                else:
                    feature.extend([0, 0, 0])
            features.append(feature)
            labels.append(self.labelsMap[item['signal']])
            
        return features, labels
                
        
    # Each entry has numBowEntries, for each word we have sum of 3 scores: "+" + "-" + "obj" if the word exists in the sentence, else 0
    def ExtractBoWSentiWordNetCollectiveFeatures(self, dataSet, bow):
        
        # Initialize the features and labels
        features = []
        labels = []
        
        # Score the features against the dataset
        for item in dataSet:
            feature = []
            for senti_word in bow:                
                if senti_word in item['headline'].split(' '):
                    feature.extend([senti_word['pos_score'] + senti_word['neg_score'] + senti_word['obj_score']])
                else:
                    feature.extend([0])
            features.append(feature)
            labels.append(self.labelsMap[item['signal']])
            
        return features, labels 
    
    # For each sentence, sum 3 scores for all the words if found in senti word net
    def ExtractCollectiveLexiconSentimentFeatures(self, dataSet):
        
        # Initialize the features and labels
        features = []
        labels = []
        
        # Score the features against the dataset
        for item in dataSet:
            pos_score = 0
            neg_score = 0
            obj_score = 0                
            for word in item['headline'].split(' '):                
                try:
                    syn = self.swn.senti_synset(word)

                    pos_score = pos_score + syn.pos_score
                    neg_score = neg_score + syn.neg_score
                    obj_score = obj_score + syn.obj_score
                    
                except:
                    # No entry in Senti WordNet
                    continue
                
            features.append([pos_score, neg_score, obj_score])
            labels.append(self.labelsMap[item['signal']])
            
        return features, labels 