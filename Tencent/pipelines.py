# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sqlite3


class TencentPipeline(object):
    def process_item(self, item, spider):
        return item


class TencentSQLitePipeline(object):
    def __init__(self):
        self.createDB()

    def createDB(self):
        self.con = sqlite3.connect(os.getcwd() + '\\db.sqlite3')
        self.cur = self.con.cursor()

    def saveData(self, item):
        #添加zhaopin_worklocation
        self.cur.execute('select * from zhaopin_worklocation WHERE name="%s"' % (item['workLocation']))
        res1 = self.cur.fetchone()
        if res1 == None:
            self.cur.execute('insert into zhaopin_worklocation (name) VALUES ("%s")' % (item['workLocation']))
            self.con.commit()
            #若不存在,添加之后再次查询,获取id
            self.cur.execute('select * from zhaopin_worklocation WHERE name="%s"' % (item['workLocation']))
            res1 = self.cur.fetchone()
        worklocation_id = res1[0]

        # 添加zhaopin_category
        self.cur.execute('select * from zhaopin_category WHERE name="%s"' % (item['category']))
        res2 = self.cur.fetchone()
        if res2 == None:
            self.cur.execute('insert into zhaopin_category (name) VALUES ("%s")' % (item['category']))
            self.con.commit()
            self.cur.execute('select * from zhaopin_category WHERE name="%s"' % (item['category']))
            res2 = self.cur.fetchone()
        category_id=res2[0]


        sql = 'insert into zhaopin_zhaopin (title,content,peopleNumber,workLocation_id,publishTime,category_id,author_id) VALUES("%s","%s","%s","%s","%s","%s","%s")' % (
            item['title'], item['content'], item['peopleNumber'], worklocation_id, item['publishTime'],
            category_id,0)
        self.cur.execute(sql)
        self.con.commit()

    def process_item(self, item, spider):
        self.saveData(item)
        return item

    def __del__(self):
        self.cur.close()
        self.con.close()
