# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class XueqiuItem(Item):
    # define the fields for your item here like:
    id = Field()
    screen_name = Field()
    gender = Field()
    province = Field()
    city = Field()

    cube_count = Field()
    followers_count = Field()
    friends_count = Field()
    last_status_id = Field()
    status_count = Field()
    stocks_count = Field()
    verified = Field()
    verified_type = Field()

    friendship = Field()

