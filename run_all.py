import redis   # 导入redis模块，通过python操作redis 也可以直接在redis主机的服务端操作缓存数据库
import os
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from cvs_scrapy import settings as my_settings
from cvs_scrapy.items import CvsScrapyItem
from cvs_scrapy.spiders.familymart import Familymart
from cvs_scrapy.spiders.hilife import Hilife

crawler_settings = Settings()
crawler_settings.setmodule(my_settings)

process = CrawlerProcess(settings=crawler_settings)
#process.crawl(Familymart)
process.crawl(Hilife)

process.start() # the script will block here until all crawling jobs are finished

r = redis.Redis(host='redis', port=6379, decode_responses=True,password=os.getenv("REDISPWD"))   # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
#r.set('name', 'junxi')  # key是"foo" value是"bar" 将键值对存入redis缓存
#print(r['name'])
print(r.get('北市正寶店'))  # 取出键name对应的值
print(r.get('02-23705368'))
print(r.lrange('hilife',0,-1))
print(type(r.get('北市正寶店')))
