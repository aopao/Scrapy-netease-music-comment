# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from yinyue.items import ArtistItem


class ArtistSpider( scrapy.Spider ) :
    name = 'artist'
    allowed_domains = ['163.com']
    start_urls = []
    # 华语
    huayu_id = [1001 , 1002 , 1003]
    # 欧美
    oumei_id = [2001 , 2002 , 2003]
    # 日本
    riben_id = [6001 , 6002 , 6003]
    # 韩国
    hanguo_id = [4001 , 4002 , 4003]
    # 其他
    qita_id = [7001 , 7002 , 7003]
    cat_id = huayu_id  + oumei_id + riben_id + hanguo_id + qita_id
    cat_url = 'http://music.163.com/discover/artist/cat?id={0}&initial={1}'

    def start_requests( self ) :
        for id in self.cat_id :
            for num in range( 65 , 91 ) :
                url = self.cat_url.format( id , num )
                yield Request( url = url , callback = self.parse )

    def parse( self , response ) :
        print( '正在下载的页面:' , response.url )
        for node in response.xpath( '//ul[@id="m-artist-box"]/li' ) :
            item = ArtistItem()
            artist_id = node.xpath( './/a[1]/@href' ).extract_first()[11 :]
            artist = node.xpath( './/a[1]/@title' ).extract_first()[:-3]
            item['artist_id'] = artist_id
            item['artist'] = artist
            print( artist_id , '-----' , artist )
            yield item
