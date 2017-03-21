#!/usr/bin/python
# -*- coding:utf-8 -*-
import codecs
import json

import scrapy
import re
from scrapy import log
from ibtibt.items import IbtibtItem
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc


class IbtibtSpider(scrapy.Spider):
    name = "ibtibt"
    allowed_domains = ["www.ibtibt.com", "movie.douban.com"]
    start_urls = [
        "http://www.ibtibt.com/html/1080p/wx/Index.Html"
    ]

    def parseDouBanImg(self, response):
        item = response.meta['item']
        item["image_urls"] = "https://img1.doubanio.com/view/photo/photo/public/p" + re.compile(
            'https://movie.douban.com/photos/photo/(.*?)/').findall(
            response.xpath('//div[@class="cover"]/a/@href').extract()[0])[0] + ".webp"
        yield item

    def parseDouBanDetail(self, response):
        item = response.meta['item']
        base_url = get_base_url(response)
        item["director"] = response.xpath('//span[@class="attrs"]').extract()
        item["title"] = response.xpath('//span[@property="v:itemreviewed"]/text()').extract()
        item["director"] = response.xpath(u'//span[text()="导演"]/following-sibling::span/a/text()').extract()
        item["scenarist"] = response.xpath(u'//span[text()="编剧"]/following-sibling::span/a/text()').extract()
        item["actor"] = response.xpath(u'//span[text()="主演"]/following-sibling::span/a/text()').extract()
        item["mtype"] = response.xpath(
            u'//span[text()="类型:"]/following-sibling::span[@property="v:genre"]/text()').extract()
        item["releaseDate"] = response.xpath(u'//span[@property="v:initialReleaseDate"]/text()').extract()
        item["runtime"] = response.xpath(u'//span[@property="v:runtime"]/text()').extract()
        item["IMDburl"] = response.xpath(u'//span[text()="IMDb链接:"]/following-sibling::a/@href').extract()
        item["doubanScore"] = response.xpath(u'//strong[@property="v:average"]/text()').extract()
        item["doubanScoringNum"] = response.xpath(u'//span[@property="v:votes"]/text()').extract()
        item["douban5Star"] = response.xpath(
            '//span[@class="stars5 starstop"]/following-sibling::span/text()').extract()
        item["douban4Star"] = response.xpath(
            '//span[@class="stars4 starstop"]/following-sibling::span/text()').extract()
        item["douban3Star"] = response.xpath(
            '//span[@class="stars3 starstop"]/following-sibling::span/text()').extract()
        item["douban2Star"] = response.xpath(
            '//span[@class="stars2 starstop"]/following-sibling::span/text()').extract()
        item["douban1Star"] = response.xpath(
            '//span[@class="stars1 starstop"]/following-sibling::span/text()').extract()
        item["desc"] = response.xpath('//span[@property="v:summary"]/text()').extract()
        item["regions"] = re.compile(u'<span class="pl">制片国家/地区:</span>(.*?)<br>').findall(
            response.xpath(u'//div[@id="info"]').extract()[0])
        item["language"] = re.compile(u'<span class="pl">语言:</span>(.*?)<br>').findall(
            response.xpath(u'//div[@id="info"]').extract()[0])
        item["othertitle"] = re.compile(u'<span class="pl">又名:</span>(.*?)<br>').findall(
            response.xpath(u'//div[@id="info"]').extract()[0])
        item["doubanUrl"] = base_url
        imgs = response.xpath('//a[@class="nbgnbg"]/@href').extract()
        for img in imgs:
            yield scrapy.Request(img,
                                 meta={'item': item}, callback=self.parseDouBanImg)

    def parseDouBanSearchback(self, response):
        item = response.meta['item']
        item["title"] = response.xpath('//title/text()').extract()
        ids = response.xpath('//div[starts-with(@id,"collect_form_")]/@id').extract()
        detailid = ids[0].split('_')[2]
        item["id"] = detailid
        yield scrapy.Request("https://movie.douban.com/subject/%s/" % detailid,
                             meta={'item': item}, callback=self.parseDouBanDetail)

    def parseDouBanSearch(self, response):
        item = response.meta['item']
        base_url = get_base_url(response)
        base_url = base_url.replace("https://movie.douban.com/j/subject_suggest?q=",
                                    "https://movie.douban.com/subject_search?search_text=")
        jsonresponse = json.loads(response.body_as_unicode())
        if len(jsonresponse) == 0:
            yield scrapy.Request(base_url,
                                 meta={'item': item}, callback=self.parseDouBanSearchback)
        else:
            yield scrapy.Request(jsonresponse[0]["url"],
                                 meta={'item': item}, callback=self.parseDouBanDetail)

    def filmDetail(self, response):
        item = IbtibtItem()
        title = response.xpath('//div[@class="content_p"]/h1//text()').extract()
        desc = response.xpath('//div[@class="c_neirong"]').extract()
        item["title"] = title
        item["ibttitle"] = title
        item["ibtdesc"] = desc
        for filmname in title:
            if filmname.find('][') == -1:
                filmname = filmname.split()[2]
            else:
                filmname = filmname.split('][')[2].split()[0]
            yield scrapy.Request("https://movie.douban.com/j/subject_suggest?q=%s" % filmname,
                                 meta={'item': item}, callback=self.parseDouBanSearch)
            # yield item

    def parse(self, response):
        base_url = get_base_url(response)
        for sel in response.xpath('//div[@class="l_list"]/ul/li'):
            link = sel.xpath('a/@href').extract()
            for url in link:
                yield scrapy.Request(urljoin_rfc(base_url, url), callback=self.filmDetail)

                # for url in response.xpath(u'//a[text()="下一页"]/@href').extract():
                #     yield scrapy.Request(urljoin_rfc(base_url, url), callback=self.parse)
                # for meurl in response.xpath(u'//span[@class="topmenu"]/ul/li').extract():
                #     link = sel.xpath('a/@href').extract()
                #     yield scrapy.Request(urljoin_rfc(base_url, link), callback=self.parse)
