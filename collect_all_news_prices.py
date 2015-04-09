import os
import csv
from DatasetBuilder.DatasetBuilder import DatasetBuilder

prices = []
news_headlines = []
def CollectNews():  
    dirName = '.\\crawler\\news'
    for file in os.listdir(dirName):        
        if file.endswith(".csv"):
            full_file_name = dirName + '\\' + file
            
            d.csvNewsFileName = full_file_name
            
            news_headlines.extend(d.get_news_headlines())
            
def CollectPrices():    
    dirName = '.\\crawler\\prices'
    for file in os.listdir('.\\crawler\\prices'):        
        if file.endswith(".csv"):
            full_file_name = dirName + '\\' + file
            
            d.csvPricesFileName = full_file_name
            
            prices.extend(d.get_prices())                
            
            
d = DatasetBuilder()

CollectNews()
CollectPrices()
d.csvNewsFileName = 'news_all.csv'
d.DumpNewsCSV(news_headlines)
d.csvPricesFileName = 'prices_all.csv'
d.DumpPricesCSV(prices)
