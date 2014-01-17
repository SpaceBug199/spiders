#
#       nice litle spoder that scrapes content from mylifetime pregnancy news feed
#       give it some cookies and milk and it  will give you a finger :/
#
import re
import datetime
import time
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
        
         # set ( 0 , 1) for latest news and set 12+ for all articles, page numers are null indexed 
        for page in range(0, 1): 
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
            # set callback for function and pass arg to it
            cb = lambda response: self.get_content(response, domain + link)
            yield Request(domain + link, callback = cb)
        
        
        

    def get_content(self, response, link):
        # strip firt two paragraphs form article page, also scrape img url, date and author 
        print link, type(link)
        sel = Selector(response)
        contentsize = 300                   # content size defined in number of characters
        paragraph = 4
        alltext = ""    
        post = []
        # site uses node-xxxxx (x = 1-9) as article id, search content via <div class ="" ...> tags using 'contains(concat(...))' 
       
        # set variable for < div(class = "content-page clearfix") > to get content from content page
        divlocator = '//*[@id="primary-content"]//div[contains(concat(" ",normalize-space(@class)," ")," content-page clearfix ")]'
        # set variable for<div class="post-meta-information clearfix">
        bioinfo = '//*[@id="primary-content"]//div[contains(concat(" ",normalize-space(@class)," ")," post-meta-information clearfix ")]'
        # get title and extract text form it
        
        # get date from post-meta
        dates = sel.xpath(bioinfo + '/p/text()').extract()
        for dt in dates:
            date = dt
        date = self.format_date(date)    
        print date
        
        # get author image form post-meta
        autoimgs = sel.xpath(bioinfo + '/div/div/a/img/@src').extract()
        for autoimg in autoimgs:
            authorimage = autoimg
        #print authorimage
        
        # get author from post-meta
        authors = sel.xpath(bioinfo + '/div/a/text()').extract()
        for auto in authors:
            author = auto
        #print auto
        
        # get post image from post-meta
        imgs = sel.xpath('//*[@id="primary-content"]/article/div/img/@src').extract()
        for img in imgs:
            image = img
        #print image
        
        # get post title from post-meta
        titles = sel.xpath('//*[@id="primary-content"]/article/div[2]/div/h1/text()').extract()
        for tit in titles:
            title = tit
        #print title
        print self.name
        size = 0
        # iterate p tags untill you have over 9000 (sry 300 char)
        # using for loop and if statment to increse counter if char count under 300
        # avoiding while loop since number of iterations in loop is usualy less then 3
        # having predefined counter inside construction of for loop produces code with less code :P
        for pnum in range (1,paragraph):
            # selector returns a list of all string found on site defined by xpath
            xpathselector = divlocator + '/./p[' + str(pnum) + ']/text()'
            posts = sel.xpath( xpathselector + '|' + divlocator + '/./p[' + str(pnum) + ']/a/text()' + '|' + divlocator + '/./p[' + str(pnum) + ']/strong/text()').extract()
            # iterate list to extract wanted and combine strings in one unified content
            for post in posts:
                alltext += post  
                size = len(alltext)
            if size < contentsize:
                paragraph += 1
        # printing alltext on stdout will throw an error involving formating, something abot ascii or unicode characters and not being able to format
        # he is a real dick when it comes to formating and wierd string characters
        # works well when posted to mongo database 
        
        articledate = date
        botname = "mylifetime batman"
        spiderlink = "null"
        domain = 'http://moms.mylifetime.com'
        local = "US"
        
        # handle posting to db via post_to_mongodb
        self.post_to_mongodb(size, author, title, alltext, domain, link, articledate, botname, spiderlink, local)
        
        
    def post_to_mongodb(self, size, author, title, post, domain, link, articledate, botname, spiderlink, local):
        # hadle mogo db posting 
        # posting content to mongodb database
        # mongolab  login: buggy pass: h3x4p0d
        client = MongoClient ('mongodb://buggy_spider:spider@ds039507.mongolab.com:39507/buggy_test')
        db = client.buggy_test
        # format author, titile, post, from, link to source, original date of article, name of active bot, link to bot in database
        local = "null"
        db.blog.insert({"size":size, "author":author, "title":title, "post":post, "from": domain, "link": link, "article_date": articledate, "local": local, "spider_name": botname, "spider_link": spiderlink})
        print "\n posted to buggy_server, signed as", botname
        
    def format_date(self, date):
        # format a date string from date string from site (Posted on <date> - at <time>) to year-day-month, <date> = Month day, year
        date = date.split(' ', 2)[2]
        date1 = date.split(',', 1)[0] 
        date2 = ((date.split(',',1 )[1]).split('-', 1)[0]).strip()
        date = date1 + " " + date2
        date = time.strptime(date, "%B %d  %Y")
        date = time.strftime("%Y-%d-%b", date)
        return date