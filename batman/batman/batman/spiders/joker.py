import re
import datetime
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import BaseSpider
from batman.items import BatmanItem
from scrapy.http import Request
from pymongo import MongoClient

class JokerSpider(BaseSpider):
    name = 'joker'
    allowed_domains = ['www.netmums.com']
    start_urls = ['http://www.netmums.com/pregnancy/pregnancy-week-by-week-guide']

    def parse(self, response):
        url_main = "http://www.netmums.com/pregnancy/pregnancy-week-by-week-guide/"
        url_tail = "-weeks-pregnant"

        for week in range (4, 43):
            print "scraping week:" + str(week)
            # quee all sites for scraping
            yield Request(url_main + str(week) + url_tail, self.get_content)
            print "week" + str(week) + " sent for scraping \n"


    def get_content(self, response):
        content = Selector(response)
        print "processing page:"
        week_title = content.xpath('/html/head/title/text()').extract()[0]
        print week_title, type(week_title)
        all_text = ""
        context = []
        #pokupi prva tri paragrafa texta
        context.append('//*[@id="ContentLeft"]/div[2]/p[1]//text()')
        context.append('//*[@id="ContentLeft"]/div[2]/p[2]//text()')
        context.append('//*[@id="ContentLeft"]/div[2]/p[3]//text()')
        
        good_stuff = content.xpath(context[0] + '|' + context[1] + '|' + context[2]).extract()
        br = 0
        # ocisti tekst i napravi dobar encoding
        for stuff in good_stuff:
            text = good_stuff[br]
            br += 1
            print text, type(text)             # debug
            text.encode('utf-8', 'ignore')
            all_text += text
            #print all_text#, type(all_text)    # debug 
            #stuff.encode('utf-8', 'ignore')    # debug
       
        main_title = content.xpath('//*[@id="ContentLeft"]/div[2]/h2/text()').extract()
       # self.post_to_mongodb(week_title, main_title, all_text)

    def post_to_mongodb(self, week_title, main_title, good_stuff):
        # hadle mogo db posting 
        client = MongoClient ('mongodb://buggy_spider:spider@ds039507.mongolab.com:39507/buggy_test')
        db = client.buggy_test
        db.blog.insert({"tjedan":week_title, "naslov":main_title, "autor":"joker", "from":"netmums", "sadrzaj":''.join(good_stuff)})
        print "\n posted to buggy_server, signed as 'joker'"