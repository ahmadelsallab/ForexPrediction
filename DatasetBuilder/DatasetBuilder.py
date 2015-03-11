'''
Created on Mar 11, 2015

@author: aelsalla
'''
import datetime

class DatasetBuilder(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def BuildDataSet(self, testSetShare):
        aligned_data_set = self.align_news_prices()
        self.trainSet, self.testSet = self.split_train_test(aligned_data_set, testSetShare)
        
    def get_prices(self):
        prices = []
        
        price = {}
        price['value'] = 0.0
        price['time_stamp'] = datetime.datetime.now()
        '''
        datetime.datetime( year , month , day , <hour> , < minute > second < microsecond >< tzinfo >)
        '''  
        
        prices.append(price)
              
        return prices
    
    def get_news_headlines(self):
        news_headlines = []
        headline = {}
        headline['text'] = ''
        headline['time_stamp'] = datetime.datetime.now()
        
        news_headlines.append(headline)
        
        return news_headlines


    def align_news_prices(self):
                
        # Initialize the aligned structure        
        aligned_data_set = []
        
        # Get the news headlines structure 
        news_headlines = self.get_news_headlines()
        
        # Get the prices structure
        prices = self.get_prices()
        
        # Loop on all news 1 by 1
        for headline in news_headlines:
            aligned_data_set_entry = {}
            # Search for it in the prices list
            # note: the prices list is sorted
            for price in prices:
                if headline['time_stamp'] >= price['time_stamp'] & headline['time_stamp'] <= price['time_stamp']:
                    # Found
                    # Set the headline text
                    aligned_data_set_entry['headline'] = headline['text']
                    
                    # Set the associated point price
                    aligned_data_set_entry['price'] = price['value']
                    
                    
                    if(len(aligned_data_set) > 0):
                        # The list is not empty, so we need to compare to the last point price
                        last_point_price = aligned_data_set[-1]['price']
                                               
                        if(price['value'] > last_point_price):
                            aligned_data_set_entry['signal'] = 'Up'
                        elif (price['value'] < last_point_price):
                            aligned_data_set_entry['signal'] = 'Down'
                        else:
                            aligned_data_set_entry['signal'] = 'Neutral'
                            
                    else:
                        # For the first entry, the signal is always neutral
                        aligned_data_set_entry['signal'] = 'Neutral'
                        
                    aligned_data_set.append(aligned_data_set_entry)
                    break
                
        
        return aligned_data_set
        

    # Utility to randomize a list
    def randomize_list(self, origList):
        import random
        random_list = []
        # Limit the size
        random_list_size =origList.__len__()
        
        # Build the dataset randomly just from the original raw
        # Create random indices
        randIndices = random.sample(range(origList.__len__()), random_list_size)
        
        # Insert in the final dataset N=self.datasetSize random tweets from the rawData
        for index in randIndices:
            random_list.append(origList[index])
        
        return random_list
              
    def split_train_test(self, dataSet, testSetShare):
        
        # Randomize the dataSet
        random_data_set = self.randomize_list(dataSet)
        
        # Calculate the test set size
        test_set_size = int(testSetShare * dataSet.__len__())
        
        # The train_set starts from the begining until before the end by the test set size 
        train_set = random_data_set[0:dataSet.__len__() - test_set_size]
        
        # The test_set is the last number of test_set_size examples
        test_set = random_data_set[train_set.__len__():]
        
        return train_set, test_set
