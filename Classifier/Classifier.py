import numpy as np
import neurolab as nl
import pylab as pl
import operator
class Classifier(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def NNTrain(self, features, labels, plot=False):
        #self.net = nl.net.newff([[0, 1]]*len(features[0]), [len(features[0]),1])
        self.net = nl.net.newff([[0, 1]], [len(features[0]), 2])
        # Train process
        reg_train_err = self.net.train(features, labels, show=15)
        
        obtainedTargets = self.net.sim(features)
        
        i = 0
        train_err = 0
        for obtainedTarget in obtainedTargets:
            maxObtainedTarget, max_value = max(enumerate(obtainedTarget), key=operator.itemgetter(1))
            if(maxObtainedTarget != labels[i]):
                train_err = train_err + 1
            i = i + 1
        if(plot):
            self.NNPlotPerformance(train_err, labels, self.net.sim(features))
        return train_err
    
    def NNTest(self, features, desiredTargets, plot=False):
        obtainedTargets = self.net.sim(features)
        i = 0
        test_err = 0
        for obtainedTarget in obtainedTargets:
            maxObtainedTarget, max_value = max(enumerate(obtainedTarget), key=operator.itemgetter(1))
            if(maxObtainedTarget != desiredTargets[i]):
                test_err = test_err + 1
            i = i + 1
        
        if(plot):
            self.NNPlotPerformance(test_err, desiredTargets, obtainedTargets)
        return test_err
    
    def NNPlotPerformance(self, err, desiredTargets, obtainedTargets):
        pl.subplot(211)
        pl.plot(err)
        pl.xlabel('Epoch number')
        pl.ylabel('error (default SSE)')
        
        x = np.linspace(0, len(desiredTargets), len(desiredTargets))
        
        y1 = desiredTargets
        y2 = obtainedTargets
        
        pl.subplot(212)
        pl.plot(x, y1, '-', x , y2, '.')
        pl.legend(['train target', 'net output'])
        pl.show()        
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