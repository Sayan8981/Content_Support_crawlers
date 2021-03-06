# -*- coding: utf-8 -*-

# Define your item pipelines here

import MySQLdb
import os
import sys
import db_detail

class VultureHboPipeline(object):
    def __init__(self):
        self.connection=MySQLdb.connect(host=db_detail.IP_addr,user='%s'%db_detail.username,passwd='%s'%db_detail.passwd,db='%s'%db_detail.database_name,charset="utf8", use_unicode=True)
        self.cursor= self.connection.cursor()
        self.counter=0


    def process_item(self, item, spider):
        self.query="insert into {table_name} (title,year,content_category,content_available,content_defination,updated_db,Service) values (%s,%s,%s,%s,%s,%s,%s)".format(table_name=db_detail.table)
        self.cursor.execute(self.query,(item["title"],item["year"],item["content_category"],item["content_available"],item["content_defination"],item["updated_db"],item["service"]))
        self.counter+=1
        self.connection.autocommit(True)
        print("\n")
        print ("Total commit: ", self.counter)
        print("\n")
        return item
        
