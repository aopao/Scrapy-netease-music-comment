#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/5 12:38
# @Author  : Jason
# @File    : json.py
# @Software: PyCharm

import json

str = '{"a":1,"b":2}'
data = json.loads(str).get('as')
# print(data.get('a'))
# print(data.get('sd'))
# print(data['ss'])

print(data)