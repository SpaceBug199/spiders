from flash.items import FlashItem
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import Selector
class Pig(BaseSpider):
    name = 'spider_pig'
    allowed_domains = ['netmums.com']
    start_urls = ['http://www.netmums.com/bloggers/category/pregnancy']
    
    def parse(self, response): 
        # jump to all sites in category pages
        for i in range( 1, 50):
            yield Request("http://www.netmums.com/bloggers/category/pregnancy/page:"+str(i), self.get_blog_links)
    
    
    def get_blog_links(self, response):
        # make a file to store all the links
        blog_links_file = open('baby_blogs.txt', 'a')        
        blog_selector = Selector(response)
        blog_links = []
        # fill the list with blog links
        blog_links += blog_selector.xpath('//*[@id="Main"]/div/article/div/div/div/h2/a/@href').extract()
        # pull out the duplicate links
        blog_links = list(set(blog_links)) 
        # empty the list into a file
        for blog_link in blog_links:
            blog_links_file.write(blog_link)
            print blog_link 
            blog_links_file.write("\n")
            print blog_selector.xpath('/html/head/title/text()').extract()
        # close the file when you are finished
        blog_links_file.close()
        
    
    
    """
    def parse(self, response):
        
        #filename = response.url.split("/")[-2]+".txt"
        
        # stage 1 selector za odabir linkova iz glavnog izbornika
        sel = Selector(response)
        # spremi sve linkove iz glavnog izbornika u listu main_menu
        main_menu = []
        # main_menu += sel.xpath('//*[@id="NavPrimary"]/ul/li//a/@href').extract()
        main_menu += sel.xpath('//*[@id="Main"]/div/article/div/div/div/h2/a/@href').extract()
        main_menu = list(set(main_menu))
        #//*[@id="Footer"]/div/div/ul/li/a
       
        # debug opcija
        # print main_menu, type(main_menu)
        
        # otvori sve linkove iz glavnog izbornika i skoci na stanicu
        for link in main_menu:  
            # debug
            print link #, type(link)
            yield Request("http://www.netmums.com"+link, self.stage_2)
    """        
    def stage_2(self, response):
        # stage 2 selector za odabir linkova iz pod izbornika
        sel_neu = Selector(response)
        print sel_neu.xpath('/html/head/title/text()').extract()
        
        