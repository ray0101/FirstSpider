# -*- coding: utf-8 -*-

# Scrapy settings for ibtibt project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ibtibt'

SPIDER_MODULES = ['ibtibt.spiders']
NEWSPIDER_MODULE = 'ibtibt.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'ibtibt (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'ibtibt.middlewares.IbtibtSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'ibtibt.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'ibtibt.pipelines.IbtibtPipeline': 300,
}
LOG_LEVEL='DEBUG'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
DOWNLOADER_MIDDLEWARES = {
   'scrapy.contrib.pipeline.images.ImagesPipeline': 1,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}
DOWNLOAD_DELAY = 0.25
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
IMAGES_STORE = "D:\\images"
ROBOTSTXT_OBEY = False
#LOG_FILE  ="D:\\1.log"
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
