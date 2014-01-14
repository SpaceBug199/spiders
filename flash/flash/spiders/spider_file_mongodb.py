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
        contents = []
        contents.append(xselect.xpath('//*[@id="ContentLeft"]/div[2]/p | //*[@id="ContentLeft"]/div[2]/p/strong/a | //*[@id="ContentLeft"]/div[2]/ul/li | //*[@id="ContentLeft"]/div[2]/p/a').extract())
        titles = xselect.xpath(' //*[@id="ContentLeft"]/div[2]/h2/text()').extract()
        # let's post it to mongodb 
        self.post_to_mongodb(contents, titles, week_title)
        
    def post_to_mongodb(self,content, title, week_title):
        client = MongoClient ('mongodb://buggy_spider:spider@ds039507.mongolab.com:39507/buggy_test')
        db = client.buggy_test
        # post downloaded content to mongodb server
        db.blog.insert({"tjedan":week_title, "naslovi":title, "autor":"spider_pig@netmums", "sadrzaj":' '.join(content)})
        print "content sent to server"
        
        
        #//*[@id="ContentLeft"]/div[2]/ul[1]