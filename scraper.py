# -*- coding: utf-8 -*-

import requests as rq
import time
import bs4
import csv

class Amazon:

    def __init__(self,filepath):
        self.headers = headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
                                'Accept-Encoding': 'gzip, deflate',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'DNT': '1', 'Connection': 'close', 'Upgrade-Insecure-Requests': '1'}

        self.filepath=filepath
        self.send=[]
        self.base_url = "https://www.amazon.com/dp/"
        self.extracted=[]
        self.next=0
        self.source_page = ''
        self.data=[]
        self.log = 'log.txt'
        self.first=True

    def logger(self,content):
        open(self.log,'a').write(content)
        open(self.log,'a').write('\n')

    def NAVIGATE_TO_AMAZON_LINK(self):
        content = rq.get(self.base_url+self.next, headers=self.headers)
        self.source_page = content.content
        
    def RETURN_BS4_CONTENT(self):
        '''
        GIVEN A RAW HTML SOURCE PAGE, IT RETURN A PARSED SOURCE PAGE
        RETURNS BS4 OBJECT
        '''
        converted=bs4.BeautifulSoup(self.source_page,'html.parser')
        return converted
    
    
    def EXTRACT_DETAILS(self):
        '''
        EXTRACT QUANTITY AND PRICE FROM THE SOURCE PAGE 
        '''
        v=self.RETURN_BS4_CONTENT()

        #amazon's quantity html element 
        #<div id="availability" class="a-section a-spacing-base">
        quantity =v.find('div',{'id':'availability'}).text.replace('\n','')

        #amazon's price html element 
        #<span id="priceblock_ourprice" class="a-size-medium a-color-price priceBlockBuyingPriceString">$16.59</span>
        price = v.find('span',{'id':'priceblock_ourprice'}).text.replace('\n','')
        
        self.data.append({'sku':self.next,'price':price,'quantity':quantity})
        #print(self.next)
        
        
    
    def main(self):

        total = 0
        #path to the csv file 
        f=open(self.filepath,'r').read()
        #print(f)
        
        for i in f.splitlines():
            if total ==0:
                total+=1
            else:
                self.next=i.split(',')[0]
                
                #Get the page 
                self.NAVIGATE_TO_AMAZON_LINK()
                try:
                    #Optional waiting 3 seconds between requests 
                    #time.sleep(3)
                    #EXTRACT AND WRITE SELF.DATA TO CSV
                    self.EXTRACT_DETAILS()
                    self.WRITE_TO_FILE()
                    print(total,' ',self.next)
                    total+=1
                except Exception as e:
                    #Handle Error saving to log
                    #Save the page 

                    self.logger('Row '+str(total)+' '+self.next.split(',')[0]+" Failed ")
                    self.logger('Error '+str(e))
                    total+=1
                    
                

         
    def WRITE_TO_FILE(self):
        keys = self.data[0].keys()
        with open('output.csv', 'a', newline='')  as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            if self.first:
                dict_writer.writeheader()
                self.first=False
            dict_writer.writerows(self.data)
        self.data=[]
       
def Start(csv_path):
    A=Amazon(csv_path)
    #start the scraper
    A.main()
    #print('called')

Start('skus.csv')
