# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class StackItem(Item):
    commentId = Field()
    against = Field()
    createTime = Field()
    vote = Field()
    userLocation = Field()
    userNickname = Field()
    userId = Field()
    content = Field()
    newsId = Field()
