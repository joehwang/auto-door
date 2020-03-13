import scrapy
import time
from scrapy.http import FormRequest
from cvs_scrapy.items import CvsScrapyItem
class Okmart(scrapy.Spider):
    name = "okmart"
    DEBUG=0
    _citys=[]
    def start_requests(self):
        urls = [
            'https://www.okmart.com.tw/convenient_shopSearch'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        time.sleep(2)
        self._citys=self.get_citys(response)
        self.log("--------------")
        self.log("列出所有縣市:{}".format(self._citys))
        #self._citys=["台中市","台南市"]
        for city in self._citys:
            yield  scrapy.Request(url='http://www.okmart.com.tw/convenient_shopSearch_Result.aspx?city={}'.format(city),
                                  callback=self.get_city_of_shop)
            if self.DEBUG==1:
                return
        self.log("***********")
    def get_citys(self,response):
        citys=response.xpath('//*[@class="shopCity"]/select[1]/option/text()').extract()
        citys.pop(0)
        return citys


    def get_city_of_shop(self,response):
        self.log("店鋪列表")

        item = CvsScrapyItem()
        for row in response.xpath('//ul/li'):
            #self.log(tr.xpath('td[1]/img[@title]/@title').extract())
            item["serial"]=row.xpath('div/a[@href]/@href').re_first(r'\(\'(.*)\',')
            item["name"]=row.xpath('h2/text()').get().strip()
            item["phone"]=""
            item["addr"]=row.xpath('span/text()').get()
            item["note"]=""
            yield item