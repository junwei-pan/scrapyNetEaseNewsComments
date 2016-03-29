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
import urllib2

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
            callback = 'parseAllCommentUrls',
            follow = True,
            process_links = 'linkNews2linkComments',
        ),
        Rule(
            LinkExtractor(allow = r'http:\/\/news\.163\.com\/\d{2}\/\d{4}\/\d{2}\/(.*)\.html'),
            callback = 'parseNews',
            follow = True,
        ),
    )

    def newsID2linkComments(self, newsId, index):
        url =  "http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/" + newsId + "/comments/newList?offset=" + str(index) + "&limit=30&showLevelThreshold=72&headLi    mit=1&tailLimit=2&callback=getData&ibc=newspc&_=1458939446003"
        return url
    
    def parseAllCommentUrls(self, response):
        '''
        For each newsId, get the list of all comments links.
        We can get the tatal number of comments links by the "newListSize" fields of the json data.
        '''
        url = response.url
        log.msg("parseAllCommentUrls")
        log.msg("url: " + url)
        newsId = pattern2.match(url).group(1)
        lst_res = response.xpath('//p').extract()
        for res in lst_res:
            item = StackItem()
            json_string = json.loads(res[11:-6])
            newListSize = json_string['newListSize']
            print 'newListSize', newListSize
            for i in range(newListSize / 30):
                urlNew = self.newsID2linkComments(newsId, i * 30)
                yield Request(urlNew, callback = self.parse_item)

    def linkNews2linkComments(self, links):
        log.msg("linkNews2linkComments")
        ret = []
        for link in links:
            newsId = pattern.match(link.url).group(1)
            ret.append(Link(self.newsID2linkComments(newsId, 0)))
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

        def parseNews(self, response):
            newsId = pattern2.match(url).group(1)
            title = response.xpath('//title/text()').extract()[0]
            keywords = response.xpath("//meta[@name='keywors']/text()").extract()[0]
            descriptions = response.xpath("//meta[@name='description']/text()").extract()[0]
            authors = response.xpath("//meta[@name='keywors']/text()").extract()[0]
            Copyrights = response.xpath("//meta[@name='keywors']/text()").extract()[0]
            content = ''.join(response.xpath("//div[@id='endText']/p/text()").extract())
