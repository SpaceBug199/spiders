import datetime
import re
import datetime
from flash.items import FlashItem
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import Selector
from pymongo import MongoClient



class Pig(BaseSpider):
    name = 'spider_pig'
    allowed_domains = ['netmums.com']
    start_urls = ['http://www.netmums.com/pregnancy/pregnancy-week-by-week-guide']
    
   
    
    def parse(self, response):
        
        sel = Selector(response)
        # format site url for fro loop to increment from week 4 to week 42
        url_main = "http://www.netmums.com/pregnancy/pregnancy-week-by-week-guide/"
        url_tail = "-weeks-pregnant"
        # increment week from week 4 to week 42
        for week in range(4,6):  
            print "scraping content for week" + str(week)
            # process each week in function get_content
            yield Request(url_main+str(week)+url_tail, self.get_content)
            print "done scraping for week " + str(week) + " \n going to next week"
            print "\n"
            
    
    
    
    def get_content(self, response):
        # extract content from site
        # start with <p> tags from content and end with <h2> tags for titles
        xselect = Selector(response)
        print "currently scraping page: "
        week_title = xselect.xpath('/html/head/title/text()').extract()
        print week_title
        print "\n"
        contents = "netmums.com contents : "
        contents = list(contents)
        head = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head><body>'
        
        contents.append(head)
        # get content and put it in list to send to mongo db
        #contents += xselect.xpath('//*([@id="ContentLeft"]/div[2]/ul[2]|//*[@id="ContentLeft"]/div[2]/p/text()|//*[@id="ContentLeft"]/div[2]/p/strong/a/text()|//*[@id="ContentLeft"]/div[2]/ul[2]/li/text()|//*[@id="ContentLeft"]/div[2]/ul[2]/li/strong/text()|//*[@id="ContentLeft"]/div[2]/p/a/text()').extract()
        #contents.append(xselect.xpath('//*[@id="ContentLeft"]/div[2]/p|//*[@id="ContentLeft"]/div[2]/p/strong/a|//*[@id="ContentLeft"]/div[2]/ul/li|//*[@id="ContentLeft"]/div[2]/ul/li/strong|//*[@id="ContentLeft"]/div[2]/p/a').extract())
        site = ''.join(xselect.xpath('//*[@id="ContentLeft"]/div[2]/p|//*[@id="ContentLeft"]/div[2]/p/strong/a/text()|//*[@id="ContentLeft"]/div[2]/ul/li|//*[@id="ContentLeft"]/div[2]/ul/li/strong|//*[@id="ContentLeft"]/div[2]/p/a/text()').extract())#.strip()
        #contents = list(set(contents))
        # take all the titles
        
        s = "Example String"
        newsite = re.sub(r'<img\s(.+=".+"\s)+''></img>', '', site)
        print newsite
        
        
        
        tail = '</body></html>'
        contents.append(tail) 
        titles = xselect.xpath(' //*[@id="ContentLeft"]/div[2]/h2/text()').extract()
        # let's post it to mongodb 
        self.post_to_mongodb(site, titles, week_title)
        
    def post_to_mongodb(self,content, title, week_title):
        client = MongoClient ('mongodb://buggy_spider:spider@ds039507.mongolab.com:39507/buggy_test')
        db = client.buggy_test
        # post downloaded content to mongodb server
        db.blog.insert({"tjedan":week_title, "naslovi":title, "autor":"spider_pig@netmums", "sadrzaj":content})
        print "content sent to server"
        
        
       
        
import re
from flash.items import FlashItem
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import Selector
from pymongo import MongoClient



class Pig(BaseSpider):
    name = 'spider_pig'
    allowed_domains = ['netmums.com']
    start_urls = ['http://www.netmums.com/pregnancy/pregnancy-week-by-week-guide']
    
   
    
    def parse(self, response):
        
        sel = Selector(response)
        # format site url for fro loop to increment from week 4 to week 42
        url_main = "http://www.netmums.com/pregnancy/pregnancy-week-by-week-guide/"
        url_tail = "-weeks-pregnant"
        # increment week from week 4 to week 42
        for week in range(4,6):  
            print "scraping content for week" + str(week)
            # process each week in function get_content
            yield Request(url_main+str(week)+url_tail, self.get_content)
            print "done scraping for week " + str(week) + " \n going to next week"
            print "\n"
            
    
    
    
    def get_content(self, response):
        # extract content from site
        # start with <p> tags from content and end with <h2> tags for titles
        xselect = Selector(response)
        print "currently scraping page: "
        week_title = xselect.xpath('/html/head/title/text()').extract()
        print week_title
        print "\n"
        
        contents = []
        
        head = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head><body>'
        
        contents.append(head)
        # get content and put it in list to send to mongo db
       
        contents.append(xselect.xpath('//*[@id="ContentLeft"]/div[2]/p|//*[@id="ContentLeft"]/div[2]/p/strong/a|//*[@id="ContentLeft"]/div[2]/ul/li|//*[@id="ContentLeft"]/div[2]/p/a').extract())
        #contents = list(set(contents))
        # take all the titles
        tail = '</body></html>'
        contents.append(tail) 
        titles = xselect.xpath('//*[@id="ContentLeft"]/div[2]/h2/text()').extract()
        # let's post it to mongodb 
        print contents
        self.post_to_mongodb(str(contents), titles, week_title)
        
    def post_to_mongodb(self,content, title, week_title):
        client = MongoClient ('mongodb://buggy_spider:spider@ds039507.mongolab.com:39507/buggy_test')
        db = client.buggy_test
        # post downloaded content to mongodb server
        db.blog.insert({"tjedan":week_title, "naslovi":title, "autor":"spider_pig@netmums", "sadrzaj":''.join(content)})
        print "content sent to server"
        
        
        