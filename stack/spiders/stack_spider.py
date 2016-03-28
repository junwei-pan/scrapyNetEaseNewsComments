#encoding: utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy import Spider
from scrapy.selector import Selector
from stack.items import StackItem
import scrapy
from scrapy import log
import json
import re

pattern = re.compile('http:\/\/news\.163\.com\/\d{2}\/\d{4}\/\d{2}\/(.*)\.html')
class StackSpider(Spider):
    name = "stack"
    #allowed_domains = ["stackoverflow.com"]
    allowed_domains = ["comment.news.163.com", "news.163.com"]
    start_urls = [
        "http://news.163.com/",
    ]
    
    rules = (
        Rule(
        LinkExtractor(allow = r'http:\/\/news\.163\.com\/\d{2}\/\d{4}\/\d{2}\/(.*)\.html'),
        callback = 'parseCommentContents',
        follow = True
        )
    )
    
    def parseCommentContents(self, response):
        s = "http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/BJ0SUGSK00014JB6/comments/newList?offset=0&limit=30&showLevelThreshold=72&headLimit=1&tailLimit=2&callback=getData&ibc=newspc&_=1458939446003"
        log.msg("!!!!!!")
        lst_res = Selector(response).xpath('//p').extract()
        for res in lst_res:
            item = StackItem()
            json_string = res[11:-6]
            json_data = json.loads(json_string)
            lst_id = json_data['comments'].keys()
            for id in lst_id:
                t = json_data['comments'][id]
                item['commentId'] = id
                item['content'] = t['content']
                item['against'] = t['against']
                item['vote'] = t['vote']
                item['userLocation'] = t['user']['location']
                try:
                    nickname = t['user']['nickname']
                except:
                    nickname = None
                item['userNickname']  = nickname
                try:
                    userId = t['user']['id']
                except:
                    userId = None
                item['userId'] = userId
                item['createTime'] = t['createTime']
                yield item
