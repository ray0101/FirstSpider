# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import random
import string

str= "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
print str