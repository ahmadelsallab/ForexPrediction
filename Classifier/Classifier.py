import numpy as np
import neurolab as nl
import pylab as pl
import operator
from sklearn.metrics import precision_recall_curve, roc_curve, auc, confusion_matrix, f1_score
class Classifier(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def NNTrain(self, features, labels, plot=False):
        formattedLabels = self.NNFormatLabels(labels, 2)
        self.net = nl.net.newff([[0, 1]]*len(features[0]), [len(features[0]), 2])
        #self.net = nl.net.newff([[0, 1]], [len(features[0]), 2])
        # Train process
        reg_train_err = self.net.train(features, formattedLabels, show=15)
        
        obtainedTargets = self.net.sim(features)
        
        i = 0
        train_err = 0
        maxObtainedTargets = []
        probs = []
        for obtainedTarget in obtainedTargets:
            maxObtainedTarget, max_value = max(enumerate(obtainedTarget), key=operator.itemgetter(1))
            maxObtainedTargets.append(maxObtainedTarget)
            probs.append(max_value)
            if(maxObtainedTarget != (labels[i] - 1)):
                train_err = train_err + 1
            i = i + 1
        if(plot):
            self.NNPlotPerformance(train_err, labels, maxObtainedTargets, probs)
        return train_err
    
    def NNTest(self, features, desiredTargets, plot=False):
        obtainedTargets = self.net.sim(features)
        i = 0
        test_err = 0
        maxObtainedTargets = []
        probs = []
        for obtainedTarget in obtainedTargets:
            maxObtainedTarget, max_value = max(enumerate(obtainedTarget), key=operator.itemgetter(1))
            maxObtainedTargets.append(maxObtainedTarget)
            probs.append(max_value)
            if(maxObtainedTarget != (desiredTargets[i] - 1)):
                test_err = test_err + 1
            i = i + 1
        
        if(plot):
            self.NNPlotPerformance(test_err, desiredTargets, maxObtainedTargets, probs)
        return test_err
    def NNFormatLabels(self, labels, nTargets):
        formatted_labels = []
        for label in labels:
            l = [0]*nTargets
            l[label-1] = 1
            formatted_labels.append(l)
        return formatted_labels
    def NNPlotPerformance(self, err, desiredTargets, obtainedTargets, probs):
        '''
        pl.subplot(211)
        pl.plot(err)
        pl.xlabel('Epoch number')
        pl.ylabel('error (default SSE)')
        
        x = np.linspace(0, len(desiredTargets), len(desiredTargets))
        
        y1 = desiredTargets
        y2 = obtainedTargets
        
        pl.subplot(212)
        pl.plot(x, y1, '-', x , y2, '.')
        pl.legend(['Target', 'net output'])
        pl.show()
        '''
        
        # Compute Precision recall curve and area the curve
        
        desiredTargets[:] = [y - 1 for y in desiredTargets]
        precision, recall, thresholds = precision_recall_curve(desiredTargets, probs)
        area = auc(recall, precision)
        print ("Area under the precision recall curve : %f" % area)
        
        # Plot Precision recall curve
        #pl.clf()
        pl.subplot(211)
        pl.plot(recall, precision, label='Precision-Recall curve')
        pl.xlabel('Recall')
        pl.ylabel('Precision')
        pl.ylim([0.0, 1.05])
        pl.xlim([0.0, 1.0])
        pl.title('Precision-Recall example: AUC=%0.2f' % area)
        pl.legend(loc="lower left")
        #pl.show()        
        
        # Compute ROC curve and area the curve
        
        fpr, tpr, thresholds = roc_curve(desiredTargets, probs)
        roc_auc = auc(fpr, tpr)
        print ("Area under the ROC curve : %f" % roc_auc)
        
        # Plot ROC curve
        #pl.clf()
        pl.subplot(212)
        pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
        pl.plot([0, 1], [0, 1], 'k--')
        pl.xlim([0.0, 1.0])
        pl.ylim([0.0, 1.0])
        pl.xlabel('False Positive Rate')
        pl.ylabel('True Positive Rate')
        pl.title('Receiver operating characteristic example')
        pl.legend(loc="lower right")
        pl.show()
        
        print(confusion_matrix(desiredTargets, obtainedTargets))
        print(f1_score(desiredTargets, obtainedTargets, average='macro'))
        
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