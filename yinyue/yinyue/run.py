#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/4 18:05
# @Author  : Jason
# @File    : run.py
# @Software: PyCharm

from scrapy.cmdline import execute

# execute('scrapy crawl artist'.split())
# execute('scrapy crawl song'.split())
execute('scrapy crawl comment'.split())
# execute("scrapy crawl song -o data.json".split())