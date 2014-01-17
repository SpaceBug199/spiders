#
#       nice litle spoder that scrapes content from mylifetime pregnancy news feed
#       give it some cookies and milk and it  will give you a finger :/
#       start with: scrapy runspider <file name>


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
    allowed_domains = ['babycenter.com']
    
    start_urls = ['http://www.babycenter.com/news']
    url_main = "http://www.babycenter.com/news?startIndex="

    def parse(self, response):
        # selects news page
        url_main = "http://www.babycenter.com/news?startIndex="
        url_tail = "&phase="
        
         
        for page in range(0, 100, 50):   # sites ar marked by article number starting at article 0 and counting 50 articles per page
            # max range at the date of creation = 1900   
            # open all available pages of articles and process with pick_article()
            print "fingering page :", page
            yield Request(url_main + str(page) + url_tail, self.pick_article)
            
            
    def pick_article(self, response):
        # selects article from news page
        print "fingered"
        # on selected page scan all articles and open each one, send for processing via get_content()
        sel = Selector(response)
        links = sel.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," newsItem ")]/b/a/@href').extract()
        #print links
        for lnk in links:
            link = str(lnk)
            # set callback for function and pass arg to it
            cb = lambda response: self.get_content(response, link)
            yield Request(link, callback = cb)
        
        
    def get_content(self, response, link):
        # strip firt two paragraphs form article page, also scrape img url, date and author 
        #print link, type(link)
        sel = Selector(response)
        contentsize = 300                   # content size defined in number of characters
        paragraph = 4
        alltext = ""  
        date = "" 
        size = 0 
        post = []
        #  search content via <div class ="" ...> tags using 'contains(concat(...))' 
       
        # set variable for < div(class = "content-page clearfix") > to get content from content page
        divlocator = '//*[contains(concat(" ",normalize-space(@class)," ")," moduleContent ")]'
        # set variable for<div class="moduleContent">
        
        # get date from post-meta
        dates = sel.xpath(divlocator + '/p[1]/text() ').extract()
        for dt in dates:
            date = dt.split(')', 1)[0]
            date = date.split('(', 1)[0]
            date = date.split(',', 1)[1]
        
        date = self.format_date(date)   
        #print date.strip()
        
        # get author image form post-meta
#        autoimgs = sel.xpath(bioinfo + '/div/div/a/img/@src').extract()
#        for autoimg in autoimgs:
#            authorimage = autoimg
        #print authorimage
        
        # get author from post-meta
#        authors = sel.xpath(bioinfo + '/div/a/text()').extract()
#        for auto in authors:
#            author = auto
        #print auto
        
        # get post image from post-meta
#        imgs = sel.xpath('//*[@id="primary-content"]/article/div/img/@src').extract()
#        for img in imgs:
#            image = img
        #print image
        
        # get post title from post-meta
        titles = sel.xpath(divlocator + '/h1/text()').extract()   
        for tit in titles:
            title = tit
        #print title
#        print self.name
#        size = 0

        # iterate p tags untill you have 'over 9000' (sry 300 char)
        # using for loop and if statment to increse counter if char count under 300
        # avoiding while loop since number of iterations in loop is usualy less then 3
        # having predefined counter inside construction of for loop produces code with less code :P
        for pnum in range (2,paragraph):
            
            # selector returns a list of all string found on site defined by xpath
            xpathselector = divlocator + '/p[' + str(pnum) + ']/text()'
            xpathselector_br = divlocator + '/br/text()'
            posts = sel.xpath( xpathselector + '|' + xpathselector_br).extract()
            # iterate list to extract wanted and combine strings in one unified content
            size = 0
            
            for post in posts:
                alltext += post  
                size = len(alltext)
            if size < contentsize:
                paragraph += 1
                
        #print alltext, "\n"
        # printing alltext on stdout will throw an error involving formating, something abot ascii or unicode characters and not being able to format
        # he is a real dick when it comes to formating and wierd string characters
        # works well when posted to mongo database 
        author = "NULL"
        articledate = date
        botname = "babycenter_spider_final"
        spiderlink = "null"
        domain = 'http://babycenter.com'
        local = "US"
        
        # handle posting to db via post_to_mongodb
        self.post_to_mongodb(size, author, title, alltext, domain, link, articledate, botname, spiderlink, local)
        
        
    def post_to_mongodb(self, size, author, title, post, domain, link, articledate, botname, spiderlink, local):
        # hadle mogo db posting 
        # posting content to mongodb database
        # mongolab  login buggy pass h3x4p0d
        client = MongoClient ('mongodb://buggy_spider:spider@ds039507.mongolab.com:39507/buggy_test')
        db = client.buggy_test
        # format author, titile, post, from, link to source, original date of article, name of active bot, link to bot in database
        local = "null"
        db.blog.insert({"size":size, "author":author, "title":title, "post":post, "from": domain, "link": link, "article_date": articledate, "local": local, "spider_name": botname, "spider_link": spiderlink})
        print "\n posted to buggy_server, signed as", botname
        
    def format_date(self, date):
        # format a date string from date string from site (Posted on <date> - at <time>) to year-day-month, <date> = Month day, year
        #date = date.split(' ', 2)[2]
        try:
            date1 = date.split(',', 1)[0] 
            date2 = date.split(',', 1)[1]
            date = date1 + date2
            date = date.strip()
            date = time.strptime(date, "%b %d  %Y")
            date = time.strftime("%Y-%d-%b", date)
        except(IndexError):
            pass
        return date