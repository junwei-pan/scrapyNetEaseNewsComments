# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import  Response, Request
from stack.items import StackItem
from scrapy.selector import Selector
import json
import re
from scrapy import log
from scrapy.link import Link
from urllib2 import urlopen

pattern = re.compile('http:\/\/news\.163\.com\/\d{2}\/\d{4}\/\d{2}\/(.*)\.html')
pattern2 = re.compile('http:\/\/comment\.news\.163\.com\/api\/v1\/products\/a2869674571f77b5a0867c3d71db5856\/threads\/(.*)\/comments')

class StackCrawlerSpider(CrawlSpider):
    name = 'stack_crawler'
    allowed_domains = ["comment.news.163.com", "news.163.com"]
    start_urls = [
        "http://news.163.com/",
    ]

    rules = (
        Rule(
            LinkExtractor(allow = r'http:\/\/news\.163\.com\/\d{2}\/\d{4}\/\d{2}\/(.*)\.html'),
            callback = 'parse_item',
            follow = True,
            process_links = 'linkNews2linkComments',
        ),
    )
    url = "http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/BJ96KRI20001124J/comments/newList?offset=0&limit=30&showLevelThreshold=72&headLi    mit=1&tailLimit=2&callback=getData&ibc=newspc&_=1458939446003"
    s = urlopen(url).read()
    print '==> s <==', s

    def newsID2linkComments(self, newsId, index):
        url =  "http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/" + newsId + "/comments/newList?offset=" + str(index) + "&limit=30&showLevelThreshold=72&headLi    mit=1&tailLimit=2&callback=getData&ibc=newspc&_=1458939446003"
        return url
    
    def getAllCommentUrls(self, newsId):
        '''
        For each newsId, get the list of all comments links.
        We can get the tatal number of comments links by the "newListSize" fields of the json data.
        '''
        urlFirstComment = self.newsID2linkComments(newsId, 0)
        log.msg('urlFirstComment: ' + urlFirstComment)
        response = urlopen(urlFirstComment)
        json_string = response.read()[9:-3]
        print 'json_string', json_string
        newListSize = json_string['newListSize']
        lst_url = []
        for i in range(newListSize / 30):
            lst_url.append(self.newsID2linkComments(newsId, i * 30))
        return lst_url

    def linkNews2linkComments(self, links):
        log.msg("linkNews2linkComments")
        ret = []
        for link in links:
            newsId = pattern.match(link.url).group(1)
            log.msg("newsId: " + newsId)
            ret.extend([Link(url) for url in self.getAllCommentUrls(newsId)])
        return ret
    
    def parse_item(self, response):
        url = response.url
        log.msg("url: " + url)
        newsId = pattern2.match(url).group(1)
        lst_res = response.xpath('//p').extract()
        for res in lst_res:
            item = StackItem()
            json_string = res[11:-6]
            json_data = json.loads(json_string)
            lst_id = json_data['comments'].keys()
            for id in lst_id:
                t = json_data['comments'][id]
                item['commentId'] = id
                item['newsId'] = newsId
                print 'id', id
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
