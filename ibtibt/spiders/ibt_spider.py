#!/usr/bin/python
# -*- coding:utf-8 -*-
import codecs
import json
import random
import string

import scrapy
import re
from scrapy import log
from ibtibt.items import IbtibtItem
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc


class IbtibtSpider(scrapy.Spider):
    name = "ibtibt"
    handle_httpstatus_list = [404, 403,301,302]
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Host': 'movie.douban.com',
        'Pragma': 'no-cache',
        'Cookie': 'bid=pVf408qdpk0;',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }
    COOKIES = {
        'bid': '87FdnWaHw6A',
        'll': '118111',
        'ct': 'y',
        'as': 'https://sec.douban.com/b?r=https%3A%2F%2Fmovie.douban.com%2Fsubject%2F4109734%2F',
        'ps': 'y',
        'dbcl2': '159373463:tQs2ag+DOoA',
        'ck': '3zvm',
        '_pk_ref.100001.4cf6': '%5B%22%22%2C%22%22%2C1490103903%2C%22https%3A%2F%2Fwww.douban.com%2Fdoulist%2F1026413%2F%22%5D',
        '_pk_id.100001.4cf6': 'a1eba458136d1f3a.1483017579.5.1490103917.1490101244.',
        '_pk_ses.100001.4cf6': '*; __utma=30149280.842103950.1481022513.1490101178.1490103904.6',
        '__utmb': '30149280.0.10.1490103904; __utmc=30149280',
        '__utmz': '30149280.1486292484.3.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
        '__utma': '223695111.1966729787.1483017579.1490101178.1490103904.6',
        '__utmb': '223695111.0.10.1490103904',
        '__utmc': '223695111',
        '__utmz': '223695111.1486292507.3.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/doulist/1026413/',
        '_vwo_uuid_v2': '6623548EDB39B3017881D81387FF07AF|3b3d306ad9acfd8296af79225f4d2366'
    }
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
    def after_404(self,response):
        print 404
    def parseDouBanDetail(self, response):
        base_url = get_base_url(response)
        if response.status in self.handle_httpstatus_list:
             yield  scrapy.Request(url=base_url, callback=self.after_404)

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
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Host': 'movie.douban.com',
            'Pragma': 'no-cache',
            'Cookie': 'bid=87FdnWaHw6A; ll="108288"; ap=1; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1490161836%2C%22https%3A%2F%2Fwww.google.co.jp%2F%22%5D; _pk_id.100001.4cf6=c852cf31b88e3206.1490004156.8.1490162369.1490153908.; __utma=223695111.2013165371.1490004156.1490153798.1490161836.9; __utmz=223695111.1490091445.6.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _vwo_uuid_v2=EBCD225812C6CC422A39EFD9B8DD178C|cd12d85077ce8548a011be91040369ee; ps=y; ue="zhangshuanglei@163.com"; dbcl2="66700964:y1EmkwcerEc"; ck=QZg1; push_noty_num=0; push_doumail_num=0; __utmt=1; __utma=30149280.294683479.1489632143.1490174211.1490236927.17; __utmb=30149280.6.6.1490236927; __utmc=30149280; __utmz=30149280.1490168362.15.9.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.6670',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
        }
        yield scrapy.Request("https://movie.douban.com/subject/%s/" % detailid,
                             meta={'item': item}, headers=headers,cookies=self.COOKIES, callback=self.parseDouBanDetail)

    def parseDouBanSearch(self, response):
        item = response.meta['item']
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Host': 'movie.douban.com',
            'Pragma': 'no-cache',
            'Cookie': 'bid=87FdnWaHw6A; ll="108288"; ap=1; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1490161836%2C%22https%3A%2F%2Fwww.google.co.jp%2F%22%5D; _pk_id.100001.4cf6=c852cf31b88e3206.1490004156.8.1490162369.1490153908.; __utma=223695111.2013165371.1490004156.1490153798.1490161836.9; __utmz=223695111.1490091445.6.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _vwo_uuid_v2=EBCD225812C6CC422A39EFD9B8DD178C|cd12d85077ce8548a011be91040369ee; ps=y; ue="zhangshuanglei@163.com"; dbcl2="66700964:y1EmkwcerEc"; ck=QZg1; push_noty_num=0; push_doumail_num=0; __utmt=1; __utma=30149280.294683479.1489632143.1490174211.1490236927.17; __utmb=30149280.6.6.1490236927; __utmc=30149280; __utmz=30149280.1490168362.15.9.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.6670',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        }
        base_url = get_base_url(response)
        base_url = base_url.replace("https://movie.douban.com/j/subject_suggest?q=",
                                    "https://movie.douban.com/subject_search?search_text=")
        jsonresponse = json.loads(response.body_as_unicode())
        if len(jsonresponse) == 0:
            yield scrapy.Request(base_url,
                                 meta={'item': item}, headers=headers,cookies=self.COOKIES, callback=self.parseDouBanSearchback)
        else:
            yield scrapy.Request(jsonresponse[0]["url"],
                                 meta={'item': item}, headers=headers, cookies=self.COOKIES,callback=self.parseDouBanDetail)

    def filmDetail(self, response):
        base_url = get_base_url(response)
        item = IbtibtItem()
        title = response.xpath('//div[@class="content_p"]/h1//text()').extract()[0]
        desc = response.xpath('//div[@class="c_neirong"]').extract()
        downloadurl=response.xpath('//div[@class="c_neirong"]/div/table/tbody/tr[1]').extract()
        item["title"] = title
        item["ibttitle"] = title
        item["ibtdesc"] = desc
        item["downloadurl"] = downloadurl
        headers = {
            'Accept': '*/*',
            'Host': 'movie.douban.com',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,ja;q=0.2',
            'Pragma': 'no-cache',
            'Cookie': 'bid=87FdnWaHw6A; ll="108288"; ap=1; _vwo_uuid_v2=EBCD225812C6CC422A39EFD9B8DD178C|cd12d85077ce8548a011be91040369ee; ps=y; ue="zhangshuanglei@163.com"; dbcl2="66700964:y1EmkwcerEc"; ck=QZg1; push_noty_num=0; push_doumail_num=0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1490237426%2C%22https%3A%2F%2Fwww.google.co.jp%2F%22%5D; _pk_id.100001.4cf6=c852cf31b88e3206.1490004156.9.1490237426.1490162369.; _pk_ses.100001.4cf6=*; __utma=30149280.294683479.1489632143.1490174211.1490236927.17; __utmb=30149280.6.6.1490236927; __utmc=30149280; __utmz=30149280.1490168362.15.9.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.6670; __utma=223695111.2013165371.1490004156.1490161836.1490237426.10; __utmb=223695111.0.10.1490237426; __utmc=223695111; __utmz=223695111.1490091445.6.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
        }
        if title.find('][') == -1:
            filmnames = title.split()
            if len(filmnames) > 2:
                 filmname = title.split()[2]
            else:
                log.msg("error:"+ title)
                pass
        else:
             filmname = title.split('][')[2].split()[0]
        for sel in response.xpath('//div[@class="neirong_r"]/ul/li/a/@href').extract():
            yield scrapy.Request(urljoin_rfc(base_url, sel),callback=self.filmDetail)
        yield scrapy.Request("https://movie.douban.com/j/subject_suggest?q=%s" % filmname,
                                 meta={'item': item}, headers=headers,cookies=self.COOKIES, callback=self.parseDouBanSearch)
            # yield item

    def parse(self, response):
        base_url = get_base_url(response)
        for sel in response.xpath('//div[@class="l_list"]/ul/li'):
            link = sel.xpath('a/@href').extract()
            print link
            for url in link:
                yield scrapy.Request(urljoin_rfc(base_url, url), callback=self.filmDetail)
            for url in response.xpath(u'//a[text()="下一页"]/@href').extract():
                yield scrapy.Request(urljoin_rfc(base_url, url), callback=self.parse)
            for meurl in response.xpath(u'//span[@class="topmenu"]/ul/li/a/@href').extract():
                yield scrapy.Request(urljoin_rfc(base_url, meurl), callback=self.parse)
