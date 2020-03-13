#-*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import FormRequest
from cvs_scrapy.items import CvsScrapyItem
class Hilife(scrapy.Spider):
    name = "hilife"
    DEBUG=1
    _citys=[]
    def start_requests(self):
        urls = [
            'https://www.hilife.com.tw/storeInquiry_street.aspx'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self._citys=self.get_citys(response)
        self.log("--------------")
        self.log("列出所有縣市:{}".format(self._citys))
        for city in self._citys:
            yield  scrapy.FormRequest('https://www.hilife.com.tw/storeInquiry_street.aspx',
                                      formdata={'CITY': city,
                                                '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                                                '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first()
                                                },dont_filter=True,callback=self.get_areas_into_city)
            if self.DEBUG==1:
                return
        self.log("***********")
    def get_citys(self,response):
        return response.xpath('//*[@id="CITY"]/option/text()').extract()

    def get_areas_into_city(self,response):
        self.log("55555555555555555555555555")
        areas=response.xpath('//*[@id="AREA"]/option/text()').extract()
        city=response.xpath('//*[@id="lblCity"]/text()').extract()[0]
        self.log("{}的所有行政區{}".format(city,areas))
        for area in areas:
            self.log("查詢:{} {}".format(city,area))
            yield  scrapy.FormRequest('https://www.hilife.com.tw/storeInquiry_street.aspx',
                                          formdata={'CITY': city,
                                                    'AREA': area,
                                                    '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                                                    '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first()},
                                                     dont_filter=True,callback=self.get_area_info)
            if self.DEBUG==1:
                return
    def get_area_info(self,response):
        self.log("店鋪列表")
        self.log(response.xpath('//*[@id="wrapper"]/div[2]/div/div/table/tr/th/text()').extract())
        item = CvsScrapyItem()
        for tr in response.xpath('//*[@id="wrapper"]/div[2]/div/div/table/tr'):
            #self.log(tr.xpath('td[1]/img[@title]/@title').extract())
            item["serial"]=tr.xpath('th[1]/text()').get()
            item["name"]=tr.xpath('th[2]/text()').get()
            item["phone"]=tr.xpath('td[2]/text()').get()
            item["addr"]=tr.xpath('td[1]/a/text()').get()
            item["note"]=tr.xpath('td[1]/img[@title]/@title').extract()
            yield item