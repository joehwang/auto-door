# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import re
import os
class CvsScrapyPipeline(object):
	def open_spider(self,spider):
		self._redis = redis.Redis(host='redis', port=6379, decode_responses=True,password=os.getenv("REDISPWD"))

	def process_item(self, item, spider):
		if item.get("addr"):
			tags=re.findall(r"(\D*[縣市])?(\D*[區鎮鄉市])?(\D*[村里])?(\D*[路大道街])", item["addr"])
			item["tags"]=",".join(filter(None, [a for b in tags for a in b]))
			#(\D*[縣市])(\D*[區鎮鄉市])(\D*[路大道街])
			self._redis.set(item["name"], item["addr"])
			self._redis.set(item["phone"], item["name"])
			self._redis.lpush(item["kind"],item["name"]) 
			return item

	def close_spider(self, spider):
		pass