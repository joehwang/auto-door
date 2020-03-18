#-*- coding: utf-8 -*-
import scrapy
import time
from cvs_scrapy.items import CvsScrapyItem
import json
class Seveneleven(scrapy.Spider):
    name = "seveneleven"
    DEBUG=0
    _citys=[]
    #https://api.map.com.tw/net/familyShop.aspx?searchType=ShopList&type=&city=%E6%BE%8E%E6%B9%96%E7%B8%A3&area=%E9%A6%AC%E5%85%AC%E5%B8%82&road=&fun=showStoreList&key=6F30E8BF706D653965BDE302661D1241F8BE9EBC
    def start_requests(self):
        urls = [
            #'https://emap.pcsc.com.tw/emap.aspx#',
            'https://emap.pcsc.com.tw/lib/areacode.js'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self._citys=self.get_citys(response)
        self.log("--------------")
        self.log("列出含有7-11所有縣市:{}".format(self._citys))
        headers={'Referer':'https://emap.pcsc.com.tw/emap.aspx','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

        for city in self._citys:
            city_code=list(city.values())[0]
            city_name=list(city.keys())[0]
            #self.log(city_code) #unpack dict values

            url="https://emap.pcsc.com.tw/EMapSDK.aspx"
            yield scrapy.Request(url=url, method='POST',
                          body="commandid=GetTown&cityid={}&leftMenuChecked=".format(city_code),meta={'city_name':city_name},headers=headers,callback=self.get_dists_of_city)
            if self.DEBUG==1:
               return None


    def get_dists_of_city(self,response):
        self.log("***********")
        dicts=response.xpath('//*/GeoPosition/TownName/text()').extract()
        self.log(dicts)
        ##get the shops
        headers={'Referer':'https://emap.pcsc.com.tw/emap.aspx','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        url="https://emap.pcsc.com.tw/EMapSDK.aspx"
        for dict in dicts:
            yield scrapy.Request(url=url, method='POST',
                          body="commandid=SearchStore&city={}&town={}".format(response.meta["city_name"],dict),headers=headers,callback=self.get_shops)
            if self.DEBUG==1:
               return None

    def get_shops(self,response):
        shops=response.xpath('//*/GeoPosition')
        item = CvsScrapyItem()
        for shop in shops:
            item["serial"]=shop.xpath('POIID/text()').get().strip()
            item["name"]=shop.xpath('POIName/text()').get().strip()
            item["phone"]=shop.xpath('Telno/text()').get().strip()
            item["addr"]=shop.xpath('Address/text()').get().strip()
            item["ship_status"]=""
            item["note"]=shop.xpath('StoreImageTitle/text()').get().strip().replace(","," ")
            item["kind"]="seven"
            yield item


    def get_citys(self,response):
        #return response.xpath('//*[@id="tw"]/div/a/text()').extract()
        groups=response.xpath('//*').re(r'new AreaNode\(\'(.*)\', new bu\(.*,.*\), \'(\d\d)\'\)')
        #self.log(groups)
        a=[]
        for i in range(0,len(groups),2):
            a.append({groups[i]:groups[i+1]})
        return a
