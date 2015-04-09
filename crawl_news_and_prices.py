
from DatasetBuilder.DatasetBuilder import DatasetBuilder
import datetime, time
# Open the file


while True:
    logFile = open('crawl_log_file.txt', 'a')
    print('Crawling now ' + str(datetime.datetime.now()))
    logFile.write('Crawling now ' + str(datetime.datetime.now()) +'\n')
    logFile.close()
    d = DatasetBuilder()
    news_headlines = d.ParseNewsURL()
    
    for headline in news_headlines:
        print(headline['text'] + '\n' + headline['time_stamp'])
    
    d.csvNewsFileName = '.\\crawler\\news\\news_' + str(datetime.datetime.now().hour) +'_' + str(datetime.datetime.now().minute) + '_' + str(datetime.datetime.now().second) +'.csv'
    
    
    d.DumpNewsCSV(news_headlines)
    
    
    prices = d.ParsePricesURL()
    
    for price in prices:
        print(price['value'] + '\n' + price['time_stamp'])
    
    d.csvPricesFileName = '.\\crawler\\prices\\prices_'+ str(datetime.datetime.now().hour) +'_' + str(datetime.datetime.now().minute) + '_' + str(datetime.datetime.now().second) +'.csv'  
    d.DumpPricesCSV(prices)
    # Crawl every hour
    time.sleep(3600)