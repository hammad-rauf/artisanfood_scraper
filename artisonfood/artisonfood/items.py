# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArtisonfoodItem(scrapy.Item):

    category = scrapy.Field()
    sub_category = scrapy.Field()
    sub_sub_category = scrapy.Field()

    filters = scrapy.Field()
    sub_filters = scrapy.Field()

    pass
