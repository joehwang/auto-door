import scrapy
from scrapy.http import FormRequest
import time
class Hilife(scrapy.Spider):
    name = "hilife"
    _citys=[]
    _times=0
    def start_requests(self):
        urls = [
            'https://www.hilife.com.tw/storeInquiry_street.aspx'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self._citys=self.get_citys(response)

        self.log("--------------")
        self.log(self._citys)


        i=0
        #self.log( response.css('input#__VIEWSTATE::attr(value)').extract_first())
        for city in self._citys:
            i=i+1
            if i>3:
                return
            yield  scrapy.FormRequest('https://www.hilife.com.tw/storeInquiry_street.aspx',
                                      formdata={'CITY': city,
                                                '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                                                '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first()},
                                                 dont_filter=True,callback=self.get_areas_into_city)

        self.log("***********")

    def get_citys(self,response):
        return response.xpath('//*[@id="CITY"]/option/text()').extract()

    def get_areas_into_city(self,response):
        self.log("55555555555555555555555555")
        areas=response.xpath('//*[@id="AREA"]/option/text()').extract()
        city=response.xpath('//*[@id="lblCity"]/text()').extract()[0]
        self.log(city)
        self.log(areas)
        i=0
        for area in areas:
            i=i+1
            if i>3:
                return
            self.log("查詢:")
            self.log(city)
            self.log(area)
            yield  scrapy.FormRequest('https://www.hilife.com.tw/storeInquiry_street.aspx',
                                          formdata={'CITY': city,
                                                    'AREA': area,
                                                    '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                                                    '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first()},
                                                     dont_filter=True,callback=self.get_area_info)
    def get_area_info(self,response):
        self.log("店")
        self.log(response.xpath('//*[@id="wrapper"]/div[2]/div/div/table/tr/th/text()').extract())
