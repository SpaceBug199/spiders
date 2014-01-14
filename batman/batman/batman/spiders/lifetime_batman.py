import re
import datetime
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import BaseSpider
from batman.items import BatmanItem
from scrapy.http import Request
from pymongo import MongoClient

class JokerSpider(BaseSpider):
    name = 'mylifetime_batman'
    allowed_domains = ['moms.mylifetime.com']
    
    start_urls = ['http://moms.mylifetime.com/parenting/pregnancy']
    url_main = "http://moms.mylifetime.com/parenting/pregnancy?page="

    def parse(self, response):
        url_main = "http://moms.mylifetime.com/parenting/pregnancy?page="
        for page in range(0, 1):
        # set ( 0 , 1) for latest news and set 12+ for all articles, page numers are null indexed 
            # open all available pages of articles and process with pick_article()
            print "fingering page :", page
            yield Request(url_main + str(page), self.pick_article)
            
            
    def pick_article(self, response):
        print "fingered"
        # on selected page scan all articles and open each one, sent for processing via get_content()
        sel = Selector(response)
        links = sel.xpath('//*[@id="primary-content"]/div/div[1]/div/div/span/div[4]/p/a/@href').extract()
        domain = 'http://moms.mylifetime.com'
        #print links
        for lnk in links:
            link = str(lnk)
            print link, "\n"
            
            yield Request(domain + link, self.get_content)
        
        
        

    def get_content(self, response):
        # strip firt two paragraphs form article page, also scrape img url, date and author 
        alltext=""
        post = []
        # site uses node-xxxxx (x = 1-9) as article id, had to search content via <div class ="" ...> tags using 'contains(concat(...))' 
        sel = Selector(response)
        # set variable for < div(class = "content-page clearfix") > to get content from content page
        divlocator = '//*[@id="primary-content"]//div[contains(concat(" ",normalize-space(@class)," ")," content-page clearfix ")]'
        # iterate p tags untill you have over 9000 (sry 300 char)
        for counter in range (0,1):
            
            post = sel.xpath( divlocator + '/p[1]/text()' + '|' + divlocator + '/p[1]/a/text()').extract()
        
       
        #if len(post[0]) < 300:
           # post.append(sel.xpath(divlocator+'/p[5]/text() | /p[1]/a/text()//*[@id="node-154609"]/div[4]/p[3]').extract())
        counter = 0
        for posts in post:
            
            text = post[counter]
            #text = text.encode('utf-8', 'ignore')
            print text, type(text)
            text = text
            print text, type(text)
            counter += 1
            #text = (text.replace(u'\xa0', ' ')).encode('utf-8', 'ignore')
            print text, type(text)
            alltext += text
        
            
        

        author = "null"
        title = "null"
        domain = 'moms.mylifetime.com'
        link = "null"
        articledate = "null"
        botname = "mylifetime batman"
        spiderlink = "null"
        
        # handle posting to db via post_to_mongodb
        #self.post_to_mongodb(author, title, alltext, domain, link, articledate, botname, spiderlink)
        
        
    def post_to_mongodb(self, author, title, post, domain, link, articledate, botname, spiderlink):
        # hadle mogo db posting 
        # posting content to mongodb database
        client = MongoClient ('mongodb://buggy_spider:spider@ds039507.mongolab.com:39507/buggy_test')
        db = client.buggy_test
        # format author, titile, post, from, link to source, original date of article, name of active bot, link to bot in database
        local = "null"
        db.blog.insert({"author":author, "title":title, "post":post, "from": domain, "link": link, "article_date": articledate, "local": local, "spider_name": botname, "spider_link": spiderlink})
        print "\n posted to buggy_server, signed as", botname