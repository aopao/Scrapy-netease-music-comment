# -*- coding: utf-8 -*-
import logging
import scrapy
import pymongo
from scrapy import Request

# from song.items import ArtistItem
from yinyue.items import SongItem


class SongSpider( scrapy.Spider ) :
    name = 'song'
    start_urls = []
    artist_url = 'http://music.163.com/artist?id={0}'
    def start_requests( self ) :
        client = pymongo.MongoClient( host = '127.0.0.1' , port = 27017 )
        monogodb = client.get_database( 'music' )
        artist = monogodb.get_collection( 'artist' )
        for id in artist.find() :
            yield Request( url = self.artist_url.format( id['artist_id'] ) , callback = self.parse)

    def parse( self , response ) :
        print( '正在解析页面:' , response.url )
        if response.status != 503 :
            for node in response.xpath( '//ul[@class="f-hide"]/li' ) :
                item = SongItem()
                song_name = node.xpath( './/a/text()' ).extract_first()
                song_id = node.xpath( './/a/@href' ).extract_first()[9 :]
                item['song_name'] = song_name
                item['song_id'] = song_id
                print( song_name , '----' , song_id )
                yield item
        else :
            logging.ERROR('错误:%s' %response.url)
            with open( 'error.txt' , 'w' ) as f :
                f.write( str( response.url ) + '\n' )
