# -*- coding: utf-8 -*-
import json
import logging
import scrapy
import pymongo
import base64
import binascii
from Crypto.Cipher import AES
from scrapy import FormRequest
from yinyue.items import CommentItem


class EnParams( object ) :
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    pubKey = '010001'
    secKey = 16 * 'F'

    def aesEncrypt( self , text , secKey ) :
        pad = 16 - len( text ) % 16
        if type( text ) is str :
            text = text + pad * chr( pad )
        else :
            text = bytes.decode( text ) + pad * chr( pad )
        encryptor = AES.new( secKey , 2 , '0102030405060708' )
        ciphertext = encryptor.encrypt( text )
        ciphertext = base64.b64encode( ciphertext )
        return ciphertext

    def createParams( self , page = 1 ) :
        if page == 1 :
            text = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
        else :
            offset = str( (page - 1) * 20 )
            text = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' % (offset , 'false')
        nonce = '0CoJUm6Qyw8W8jud'
        nonce2 = 16 * 'F'
        encText = self.aesEncrypt( self.aesEncrypt( text , nonce ) , nonce2 )
        return encText

    def rsaEncrypt( self , text , pubKey , modulus ) :
        text = text[: :-1]
        rs = int( binascii.hexlify( str.encode( text ) ) , 16 ) ** int( pubKey , 16 ) % int( modulus , 16 )
        return format( rs , 'x' ).zfill( 256 )


class CommentSpider( scrapy.Spider ) :
    num = 1;
    name = 'comment'
    start_urls = []
    artist_url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{0}?csrf_token='
    en = EnParams()
    form_data = {'params' : en.createParams( 1 ) , 'encSecKey' : en.rsaEncrypt( en.secKey , en.pubKey , en.modulus )}
    headers = {
        'User-Agent' : 'android' ,
        'Cookie' : 'appver=1.5.0.75771;' ,
        'Referer' : 'http://music.163.com/'
    }

    def start_requests( self ) :
        client = pymongo.MongoClient( host = '127.0.0.1' , port = 27017 )
        monogodb = client.get_database( 'music' )
        song = monogodb.get_collection( 'song' )
        for info in song.find().skip(589280) :
            self.num += 1
            print( '%s :正在采集评论: %s' % (self.num , info['song_name']) )
            yield FormRequest(
                url = self.artist_url.format( info['song_id'] ) ,
                formdata = self.form_data ,
                headers = self.headers ,
                callback = self.parse ,
                meta = {'id' : info['song_id']}
            )

    def parse( self , response ) :
        if response.status != 503 :
            data = json.loads( response.text ).get('hotComments')
            if data:
                for info in data:
                    item = CommentItem()
                    sid = response.meta['id']
                    nickname = info['user']['nickname']
                    userId = info['user']['userId']
                    avatarUrl = info['user']['avatarUrl']
                    count = info['likedCount']
                    content = info['content']
                    commit_time = info['time']
                    item['sid'] = sid
                    item['nickname'] = nickname
                    item['userId'] = userId
                    item['avatarUrl'] = avatarUrl
                    item['count'] = count
                    item['content'] = content
                    item['commit_time'] = commit_time
                    print(sid,'-----',nickname,'-----',userId,'-----',content,'-----',commit_time,'-----',count)
                    yield item
            else:
                with open( 'error_id.txt' , 'w' ) as f :
                    f.write( str( response.url ) )
        else :
            logging.ERROR( '错误:%s' % response.url )
            with open( 'error.txt' , 'w' ) as f :
                f.write( str( response.url ) )
