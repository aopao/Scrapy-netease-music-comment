#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/4 18:18
# @Author  : Jason
# @File    : config.py
# @Software: PyCharm
import configparser


class Config( object ) :
    config_path = './config.ini'
    conf = None

    def __init__( self ) :
        self.conf = configparser.ConfigParser()
        self.conf.read( self.config_path )

    def get_all_sections( self ) :
        return self.conf.sections()

    def get_one_cat_id( self , name = 'huayu_id' ) :
        return self.conf.get( 'cat_id' , name )

    def get_all_cat_id( self ) :
        cat_id = []
        for key , id in self.conf.items( 'cat_id' ) :
            cat_id.append( id[1 :-1] )
        return list( cat_id )
