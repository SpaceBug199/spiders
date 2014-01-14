from scrapy.selector import HtmlXPathSelector
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
#from scrapy.contrib.spiders import CrawlSpider, Rule
from flash.items import FlashItem
from scrapy.spider import BaseSpider
from scrapy.http import Request
class NetmumsSpider(BaseSpider):
    name = 'netmums'
    allowed_domains = ['netmums.com']
    start_urls = ['http://www.netmums.com/']
    #
    #rules = (
    #    Rule(SgmlLinkExtractor(allow=r'/\w+'), callback='parse_item', follow=True),
    #)

    def parse(self, response):
        filename = response.url.split("/")[-2]+".txt"
        sel = HtmlXPathSelector(response)
        links = []
        #print sel.xpath('//*[@id="NavPrimary"]/ul/li//a/@href').extract()
        links += sel.select('//*[@id="NavPrimary"]/ul/li')
        links = list(set(links))
        print links, type(links)
        for link in links:
            idi = link.xpath('//a/@href').extract()
            print idi, type(idi)
            yield Request("http://www.netmums.com"+idi, self.parse2)
            
    def parse2(self, response):
        sel = HtmlXPathSelector(response)
        print sel.xpath('/html/head/title/text()').extract()
       
