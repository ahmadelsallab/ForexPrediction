'''
Created on Mar 11, 2015

@author: aelsalla
'''
import datetime
import csv
#import urllib
from bs4 import BeautifulSoup
from xml.dom import minidom
import urllib.request
import calendar
import json

class DatasetBuilder(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.csvPricesFileName = 'prices.csv'
        self.csvNewsFileName = 'news.csv'
        
    def BuildDataSet(self, testSetShare):
        aligned_data_set = self.align_news_prices()
        trainSet, testSet = self.split_train_test(aligned_data_set, testSetShare)
        
        return trainSet, testSet
        
    def get_prices(self):
        prices = []
        
        # Open csv file
        f = open(self.csvPricesFileName, 'r', encoding='UTF-8', newline='')
        # Get reader handler
        r = csv.reader(f, delimiter=',')
        
        # Skip the first row
        skip = True
        # Read the label from each row
        for row in r:
            if(not skip):
                price = {}
                
                # Price is the average
                #price['value'] = (row[1] + row[2]) / 2
                
                # Price is the close price
                price['value'] = row[0]
                
                '''
                # Read the time stamp. Skip the last 3 entries
                time_stamp_str = row[0][:-3]
                time_stamp = datetime.datetime(time_stamp_str[0:3] , time_stamp_str[4:5], time_stamp_str[6:7], time_stamp_str[9:10], time_stamp_str[11:12], time_stamp_str[13:14])
                price['time_stamp'] = time_stamp 
                '''
                
                time_stamp_str = row[1]
                time_stamp = datetime.datetime(time_stamp_str[0:3] , time_stamp_str[4:5], time_stamp_str[6:7], time_stamp_str[9:10], time_stamp_str[11:12], time_stamp_str[13:14])
                price['time_stamp'] = time_stamp 
                
                # Insert in the prices list
                prices.append(price)
            else:
                skip = False
                
        # Close the file   
        f.close()
        
        '''
        price = {}
        price['value'] = 0.0
        price['time_stamp'] = datetime.datetime.now()
        prices.append(price)
        '''
        '''
        datetime.datetime( year , month , day , <hour> , < minute > second < microsecond >< tzinfo >)
        '''  
                    
        return prices
    
    def get_news_headlines(self):
        
        news_headlines = []

        # Open csv file
        f = open(self.csvNewsFileName, 'r', encoding='UTF-8', newline='')
        # Get reader handler
        r = csv.reader(f, delimiter=',')
        
        # Skip the first row
        skip = True
        # Read the label from each row
        for row in r:
            if(not skip):
                headline = {}
                
                # Price is the average
                headline['text'] = row[0]
                
                # Read the time stamp.                
                time_stamp_str = row[1]
                time_stamp = datetime.datetime(time_stamp_str[0:3] , time_stamp_str[4:5], time_stamp_str[6:7], time_stamp_str[9:10], time_stamp_str[11:12], time_stamp_str[13:14])
                headline['time_stamp'] = time_stamp
                
                # Insert in the prices list
                news_headlines.append(headline)
            else:
                skip = False
                
        # Close the file   
        f.close()

        '''
        headline = {}
        headline['text'] = ''
        headline['time_stamp'] = datetime.datetime.now()
        
        news_headlines.append(headline)
        '''
        return news_headlines

    def traverse_historic_news(self, numDays):    
        try:
            news_headlines = []
            
            # http://finance.yahoo.com/q/h?s=EURUSD=X&t=2015-03-04
            urlstr = 'http://finance.yahoo.com/q/h?s=EURUSD=X&t='
            

            
            curr_day = datetime.date.today()
            
            one_day = datetime.timedelta(days=1)
            
            # Start from the previous day            
            curr_day = curr_day - one_day
            
            for i in range(numDays):
                
                # Append the day to the url
                day_url =  urlstr + curr_day.year + '-' + curr_day.month + '-' + curr_day.day    
                
                fileHandle = urllib.request.urlopen(day_url)
            
                html = fileHandle.read()    
            
                # For each day, parse the html
                day_headlines = self.parse_news_html(html)
            
                news_headlines.append(day_headlines)
                
                curr_day = curr_day - one_day
            
            # self.write_headlines_csv(news_headlines)
        except Exception as e:
            print('URL error ' + str(e) )

    # url = 'http://feeds.marketwatch.com/marketwatch/realtimeheadlines?format=xml'
    def ParseNewsURL(self):
        url = 'http://feeds.marketwatch.com/marketwatch/realtimeheadlines?format=xml'
        f = urllib.request.urlopen(url)
        xmldoc = minidom.parse(f)    
        
        # Get the user share balance option
        items = xmldoc.getElementsByTagName('item')
        news_headlines = []
        
        for item in items:
            headline = {}
            headline['text'] = item.getElementsByTagName('title')[0].firstChild.data
            
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
            
            headline['time_stamp'] = str(year + month + day + ' ' + hour + min + sec)
            news_headlines.append(headline)
        
        return news_headlines

    def ParsePricesURL(self):
        url = 'http://www.myfxbook.com/getHistoricalDataByDate.json?&start=2015-03-01%2000:00&end=2015-03-24%2000:00&symbol=EURUSD&timeScale=60&userTimeFormat=0&rand=0.5403805375099182'
        f = urllib.request.urlopen(url)
        json_data = json.loads(f.read().decode('utf8'))
        soup = BeautifulSoup(json_data['content']['historyData'])  
        prices = []
        for b in soup.findAll('tr', { "onmouseover" : "this.className='normalActive';" }):
            price = {}
            price['value'] = b.findAll('span', { "name" : "closeEURUSD" })[0].text.strip()
            #Mar 23, 2015 14:00
            datetime = b.findAll('span', { "name" : "timeEURUSD" })[0].text.strip()
            
            month_name = datetime.split(',')[0].split(' ')[0]
            month = str(list(calendar.month_abbr).index(month_name)).zfill(2)
            day = datetime.split(',')[0].split(' ')[1]
            
            year = datetime.split(',')[1].split(' ')[1]
            hour_min =  datetime.split(',')[1].split(' ')[2]
            hour = hour_min.split(':')[0]
            min = hour_min.split(':')[1]
            sec = '00'
            
            price['time_stamp'] = str(year + month + day + ' ' + hour + min + sec)
            prices.append(price)
        
        return prices
    
    def DumpNewsCSV(self, news_headlines):
        
        f = open(self.csvNewsFileName, 'w', newline='')
        w = csv.writer(f, delimiter=',')
        data = []
        data.append(['headline', 'time_stamp (yyyymmdd hhmmss)'])
        
        for headline in news_headlines:
            data.append([headline['text'], headline['time_stamp']])
        
        w.writerows(data)
        f.close()

    def DumpPricesCSV(self, prices):
        
        f = open(self.csvPricesFileName, 'w', newline='')
        w = csv.writer(f, delimiter=',')
        data = []
        data.append(['price', 'time_stamp (yyyymmdd hhmmss)'])
        
        for price in prices:
            data.append([price['value'], price['time_stamp']])
        
        w.writerows(data)
        f.close()      
 
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
