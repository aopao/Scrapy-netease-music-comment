# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArtistItem(scrapy.Item):
    # define the fields for your item here like:
    artist_id = scrapy.Field()
    artist = scrapy.Field()


class SongItem(scrapy.Item):
    # define the fields for your item here like:
    song_name = scrapy.Field()
    song_id = scrapy.Field()


class CommentItem(scrapy.Item):
    # define the fields for your item here like:
    #歌曲 id
    sid = scrapy.Field()

    #用户昵称
    nickname = scrapy.Field()
    #用户 id
    userId = scrapy.Field()
    #用户头像
    avatarUrl = scrapy.Field()

    #点赞数
    count = scrapy.Field()
    #歌曲评论内容
    content = scrapy.Field()
    #提交时间
    commit_time = scrapy.Field()
