# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import redis
import pymongo


class ArtistPipeline( object ) :
    def __init__( self ) :
        client = pymongo.MongoClient( host = '127.0.0.1' , port = 27017 )
        self.monogodb = client.get_database( 'music' )
        client = pymongo.MongoClient( '127.0.0.1' , 27017 )
        self.monogodb = client.get_database( 'music' )
        self.redis = redis.Redis( host = '127.0.0.1' , port = 6379 , db = 0 )

    def process_item( self , item , spider ) :
        if spider.name == 'artist' :
            if self.redis.sadd( 'artist_id' , item['artist_id'] ) :
                artist = self.monogodb.get_collection( 'artist' )
                artist.insert( {'artist_id' : item['artist_id'] , 'artist' : item['artist']} )
        elif spider.name == 'song' :
            if self.redis.sadd( 'song_id' , item['song_id'] ) :
                artist = self.monogodb.get_collection( 'song' )
                artist.insert( {'song_name' : item['song_name'] , 'song_id' : item['song_id']} )
        elif spider.name == 'comment' :
            artist = self.monogodb.get_collection( 'comment' )
            artist.insert( {
                'sid' : item['sid'] ,
                'nickname' : item['nickname'] ,
                'userId' : item['userId'] ,
                'avatarUrl' : item['avatarUrl'] ,
                'content' : item['content'] ,
                'count' : item['count'] ,
                'commit_time' : item['commit_time']
            } )
