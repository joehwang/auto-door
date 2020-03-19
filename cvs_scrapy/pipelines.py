# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re

class CvsScrapyPipeline(object):
	def process_item(self, item, spider):
		if item.get("addr"):
			tags=re.findall(r"(\D*[縣市])?(\D*[區鎮鄉市])?(\D*[村里])?(\D*[路大道街])", item["addr"])
			item["tags"]=",".join(filter(None, [a for b in tags for a in b]))
			#(\D*[縣市])(\D*[區鎮鄉市])(\D*[路大道街])
			return item
#行政區名稱	街道名稱	門牌
#縣
#市	鄉
#鎮
#縣轄市
#區	村
#里	鄰	大道
#路
#街	段	巷	弄
	def close_spider(self, spider):
		pass