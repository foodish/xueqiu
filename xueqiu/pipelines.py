# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3


class Sqlite3Pipeline(object):
    def __init__(self, sqlite_file, sqlite_table, sqlite_follow):
        self.sqlite_file = sqlite_file
        self.sqlite_table = sqlite_table
        self.sqlite_follow = sqlite_follow

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_file=crawler.settings.get('SQLITE_FILE', 'items'),  # 从 settings.py 提取
            sqlite_table=crawler.settings.get('SQLITE_TABLE'),
            sqlite_follow=crawler.settings.get('SQLITE_FOLLOW')
        )

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.sqlite_file)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    # def process_item(self, item, spider):
    #     insert_sql = "insert or ignore into {0}({1}) values ({2})".format(self.sqlite_table,
    #                                                             ', '.join(item.fields.keys()),
    #                                                             ', '.join(['?'] * len(item.fields.keys())))
    #     self.cur.execute(insert_sql, item.fields.values())
    #     self.conn.commit()

    def process_item(self, item, spider):
        insert_sql = "insert or ignore into {0} (id, screen_name, gender, province, city, " \
                     "verified, verified_type, cube_count, stocks_count, friends_count, followers_count, " \
                     "status_count, last_status_id) values (?,?,?,?,?,?,?,?,?,?,?,?,?)".format(self.sqlite_table)
        insert_follow = 'insert or ignore into {0} (user_id, friend_id) values (?,?)'.format(self.sqlite_follow)

        myitems = (item['id'], item['screen_name'], item['gender'], item['province'], item['city'],
                   item['verified'], item['verified_type'], item['cube_count'], item['stocks_count'],
                   item['friends_count'], item['followers_count'], item['status_count'], item['last_status_id'])
        myfollows = (item['friendship'][0], item['friendship'][1])

        self.cur.execute(insert_sql, myitems)
        self.cur.execute(insert_follow, myfollows)

        self.conn.commit()

        return item

class XueqiuPipeline(object):
    def process_item(self, item, spider):
        return item


