import re 
import datetime
from flash.items import FlashItem
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import Selector
from pymongo import MongoClient

class SpiderPig(BaseSpider):
    name = 'random_spiderman'
    allowed_domains = ['netmums.com']
    start_url = ['http://www.netmums.com/pregnacy/pregnancy-week-by-week-guide']
    
    def parse(self, response):
        week_selector = Selector(response)
        url_main = "http://www.netmums.com/pregnancy/pregnancy-week-by-week-guide/"
        url_tail = "-weeks-pregnant"
        # site name per week = /<week>-weeks-pregnant
        for week in range (4, 43):
            print "scraping week: " + str(week)
            # send url for each week for procesing and scraping
            yield Request(url_main+str(week)+url_tail, self.get_content)
            print "week" + str(week) + "sent to queue"
            print "\n"
            
    def get_content(self,response):
        content = Selector(response)
        print "processing page:"
        week_title = (content.xpath('/html/head/title/text()').extract()).strip()
        print week_title
        good_stuff = []
        good_stuff.append(content.xpath('//*[@id="ContentLeft"]/div[2]/p | //*[@id="ContentLeft"]/div[2]/p/strong/a/text() | //*[@id="ContentLeft"]/div[2]/ul/li | //*[@id="ContentLeft"]/div[2]/p/a/text')).extract()
        main_titles  = content.xpath('//*[@id="ContentLeft"]/div[2]/h2/text()').extract()
        self.post_to_mongodb(str(good_stuff), main_titles, week_title)
        
    def post_to_mongodb(self, content, title, week_title):
        client = MongoClient('mongodb://buggy_spider:spider@ds039507.mongolab.com:39507/buggy_test')
        db = client.buggy_test
        
        db.blog.insert({"tjedan":week_title, "naslov":title, "autor":"rundom_spider_bot", "from":"netmums", "sadrzaj":''.join(good_stuff)})
        print "\n posted to buggy server\n "