class Classifier(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    #def NNTrain(self):
    #def NNTest(self):
        
    def LexiconTest(self, features, labels):
        i = 0
        accuracy = 0
        for item in features:
            if item[0] > item[1]:
                #pos_score > neg_score
                # Up
                label = 1
            else:
                # Down
                label = 2
            
            # Did we get it right?
            if label == labels[i]:
                accuracy = accuracy + 1
            
            i = i + 1
        
        # Score the final accuracy
        return accuracy / len(features)