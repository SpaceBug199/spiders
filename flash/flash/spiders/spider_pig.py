from flash.items import FlashItem
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import Selector
class Pig(BaseSpider):
    name = 'spider_pig'
    allowed_domains = ['netmums.com']
    start_urls = ['http://www.netmums.com/']
    
    def parse(self, response):
        
        #filename = response.url.split("/")[-2]+".txt"
        
        # stage 1 selector za odabir linkova iz glavnog izbornika
        sel = Selector(response)
        # spremi sve linkove iz glavnog izbornika u listu main_menu
        main_menu = []
        # main_menu += sel.xpath('//*[@id="NavPrimary"]/ul/li//a/@href').extract()
        main_menu += sel.xpath('//*[@id="Footer"]/div/div/ul/li//a/@href').extract()
        main_menu = list(set(main_menu))
        #//*[@id="Footer"]/div/div/ul/li/a
       
        # debug opcija
        # print main_menu, type(main_menu)
        
        # otvori sve linkove iz glavnog izbornika i skoci na stanicu
        for link in main_menu:  
            # debug
            print link , type(link)
            yield Request("http://www.netmums.com"+link, self.stage_2)
            
    def stage_2(self, response):
        # stage 2 selector za odabir linkova iz pod izbornika
        sel_neu = Selector(response)
        print sel_neu.xpath('/html/head/title/text()').extract()
        
        