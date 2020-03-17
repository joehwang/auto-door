# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CvsScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    serial = scrapy.Field()
    uqid = scrapy.Field()
    kind = scrapy.Field()
    addr = scrapy.Field()
    phone = scrapy.Field()
    note = scrapy.Field()
    ship_status= scrapy.Field()

