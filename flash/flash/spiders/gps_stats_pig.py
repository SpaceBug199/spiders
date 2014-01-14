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

    def _init_():
        pass

    def parse(self, response):

        sel = Selector(response)
        # format site url for fro loop to increment from week 4 to week 42
        url_main = "http://www.netmums.com/pregnancy/pregnancy-week-by-week-guide/"
        url_tail = "-weeks-pregnant"
        # increment week from week 4 to week 42
        for week in range(4,42):
            print "scraping content for week" + week
            # process each week in function get_content
            yield Request(url_main+week+url_tail, self.get_content)
            print "done scraping for week" + week + "go to next week"
            print "\n"




    def get_content(self, response):
        # extract content from site
        # start with <p> tags from content and end with <h2> tags for titles
        xselect = Selector(response)
        print "currently scraping page:"
        print xselect.xpath('/html/head/title/text()').extract()
        print "\n"
        # get content and put it in list to send to mongo db
        contents = xselect.xpath('//*[@id="ContentLeft"]/div[2]/p/text()').extract()
        # take all the titles
        titles = xselect.xpath(' //*[@id="ContentLeft"]/div[2]/h2/text()').extract()
        # let's post it to mongodb
        self.post_to_mongodb(contents, titles)

    def post_to_mongodb(content, title):
        client = MongoClient ('mongodb://buggy:h3x4p0dX@ds039507.mongolab.com:39507/buggy_test')
        db = client.buggy_test
        # post downloaded content to mongodb server
        db.blog.insert({"naslovi":title, "autor":"spider_pig@netmums", "sadrzaj":content})
        print "content sent to server"


