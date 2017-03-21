#!/usr/bin/python
# -*- coding:utf-8 -*-
import codecs
import json

import scrapy
from ibtibt.items import IbtibtItem
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc


class IbtibtSpider(scrapy.Spider):
    name = "ibtibt"
    allowed_domains = ["www.ibtibt.com", "movie.douban.com"]
    start_urls = [
        "http://www.ibtibt.com/html/1080p/wx/Index.Html"
    ]
    def parsedoubandetail(self,response):
        item=response.meta['item']
        item["daoyan"]=response.xpath('//span[@class="attrs"]').extract()
        item["title"]=response.xpath('//span[@property="v:itemreviewed"]/text()').extract()
        yield item
    def parsedouban(self, response):
        item = response.meta['item']
        item["title"]= response.xpath('//title/text()').extract()
        ids = response.xpath('//div[starts-with(@id,"collect_form_")]/@id').extract()
        detailid = ids[0].split('_')[2]
        yield scrapy.Request("https://movie.douban.com/subject/%s/" % detailid,
                             meta={'item': item}, callback=self.parsedoubandetail)

    def parse2(self, response):
        item = IbtibtItem()
        title = response.xpath('//div[@class="content_p"]/h1/text()').extract()
        desc = response.xpath('//div[@class="c_neirong"]').extract()
        item["title"] = title
        item["desc"] = desc
        for film in title:
                film=film.split()[2]
                yield scrapy.Request("https://movie.douban.com/subject_search?search_text=%s" % film,
                                 meta={'item': item}, callback=self.parsedouban)

    def parse(self, response):
        base_url = get_base_url(response)
        print base_url
        for sel in response.xpath('//div[@class="l_list"]/ul/li'):
            link = sel.xpath('a/@href').extract()
            for url in link:
                yield scrapy.Request(urljoin_rfc(base_url, url), callback=self.parse2)

                # for url in response.xpath(u'//a[text()="下一页"]/@href').extract():
                #     yield scrapy.Request(urljoin_rfc(base_url,url),callback=self.parse)
