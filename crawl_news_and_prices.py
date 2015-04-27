
from DatasetBuilder.DatasetBuilder import DatasetBuilder
import datetime, time
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "website.settings"
from app.models import NewsHeadline, Price

# Open the file

priceStartDate = '2015-03-01'
while True:
    logFile = open('crawl_log_file.txt', 'a')
    print('Crawling now ' + str(datetime.datetime.now()))
    logFile.write('Crawling now ' + str(datetime.datetime.now()) +'\n')
    logFile.close()
    d = DatasetBuilder()
    news_headlines = d.ParseNewsURL()
    
    for headline in news_headlines:
        print(headline['text'] + '\n' + headline['time_stamp'])
        
        headline_exist = NewsHeadline.objects.filter(text=headline['text'])
        if(len(headline_exist) == 0):
            headline_entry = NewsHeadline()
            headline_entry.text = headline['text']
            headline_entry.time_stamp = headline['time_stamp']
            headline_entry.save()
    
    d.csvNewsFileName = '.\\crawler\\news\\news_' + str(datetime.datetime.now().day) +'_' + str(datetime.datetime.now().month) +'_' + str(datetime.datetime.now().year) +'_' + str(datetime.datetime.now().hour) +'_' + str(datetime.datetime.now().minute) + '_' + str(datetime.datetime.now().second) +'.csv'
    
    
    d.DumpNewsCSV(news_headlines)
    
    
    prices = d.ParsePricesURL(priceStartDate)
    
    for price in prices:
        print(price['value'] + '\n' + price['time_stamp'])
        price_exist = Price.objects.filter(time_stamp=price['time_stamp'])
        if(len(price_exist) == 0):
            price_entry = Price()
            price_entry.value = price['value']
            price_entry.time_stamp = price['time_stamp']
            price_entry.save()
    
    d.csvPricesFileName = '.\\crawler\\prices\\prices_'+ str(datetime.datetime.now().day) +'_' + str(datetime.datetime.now().month) +'_' + str(datetime.datetime.now().year) +'_' + str(datetime.datetime.now().hour) +'_' + str(datetime.datetime.now().minute) + '_' + str(datetime.datetime.now().second) +'.csv'  
    d.DumpPricesCSV(prices)
    # Crawl every hour
    time.sleep(3600)