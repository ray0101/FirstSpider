# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IbtibtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    ibttitle = scrapy.Field()
    ##导演
    director = scrapy.Field()
    ##编剧
    scenarist = scrapy.Field()
    ##演员
    actor = scrapy.Field()
    ##电影类型
    mtype = scrapy.Field()
    ##国家地区
    regions = scrapy.Field()
    ##Language
    language = scrapy.Field()
    ##上映日期
    releaseDate = scrapy.Field()
    ##片长
    runtime = scrapy.Field()
    ##othername
    othertitle = scrapy.Field()
    ##IMDb链接:
    IMDburl = scrapy.Field()
    ##豆瓣链接
    doubanUrl = scrapy.Field()
    ##豆瓣评分
    doubanScore = scrapy.Field()
    ##
    doubanScoringNum = scrapy.Field()
    douban5Star = scrapy.Field()
    douban4Star = scrapy.Field()
    douban3Star = scrapy.Field()
    douban2Star = scrapy.Field()
    douban1Star = scrapy.Field()
    ##简介
    desc = scrapy.Field()
    ##ibtibt
    ibtdesc = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    downloadurl=scrapy.Field()
