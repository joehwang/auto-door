#-*- coding: utf-8 -*-
import scrapy
import time
from cvs_scrapy.items import CvsScrapyItem
import json
class Familymart(scrapy.Spider):
    name = "familymart"
    DEBUG=0
    _citys=[]
    #https://api.map.com.tw/net/familyShop.aspx?searchType=ShopList&type=&city=%E6%BE%8E%E6%B9%96%E7%B8%A3&area=%E9%A6%AC%E5%85%AC%E5%B8%82&road=&fun=showStoreList&key=6F30E8BF706D653965BDE302661D1241F8BE9EBC
    def start_requests(self):
        urls = [
            'https://www.family.com.tw/marketing/inquiry.aspx#'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self._citys=self.get_citys(response)
        self.log("--------------")
        self.log("列出所有縣市:{}".format(self._citys))
        headers={'Referer':'https://www.family.com.tw/marketing/inquiry.aspx'}
        for city in self._citys:
            self.log(city)
            url="https://api.map.com.tw/net/familyShop.aspx?searchType=ShopList&type=&city={}&area=&road=&fun=showStoreList&key=6F30E8BF706D653965BDE302661D1241F8BE9EBC".format(city)
            yield scrapy.Request(url=url, headers=headers,callback=self.get_shop_of_citys)
            if self.DEBUG==1:
               return None
        self.log("***********")
    def get_shop_of_citys(self, response):
        
        res=response.body_as_unicode() #get RAW response
        res=res[0:len(res)-1]
        res=res.replace('showStoreList(', '')
        json_objs=json.loads(res)
        #self.log(json_objs[1])
        item = CvsScrapyItem()
        for shop in json_objs:
            yield  self.store(item,shop)
            

    def store(self,item,shop):
       # self.log(_jsonobj)
        item["serial"]=shop["pkey"]
        item["name"]=shop["NAME"]
        item["phone"]=shop["TEL"]
        item["addr"]=shop["post"]+shop["addr"]
        item["ship_status"]=""
        item["note"]=shop["all"]
        item["kind"]="familymart"
        return item
            

    def get_citys(self,response):
        return response.xpath('//*[@id="taiwanMap"]/div/a/text()').extract()
