# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from xueqiu.items import XueqiuItem
import json


class XqSpider(scrapy.Spider):
    name = "xq"
    allowed_domains = ["www.xueqiu.com"]

    start_urls = ['https://xueqiu.com/friendships/groups/members.json?page=' + str(i) + '&uid=9442520620&gid=0' for i
                  in range(1, 3)]
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    cookie = {
        'xq_a_token': 'afe4be3cb5bef00f249343e7c6ad8ac7dc0e17fb'
    }
    global id_list
    id_list = []

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers=self.headers, cookies=self.cookie, callback=self.parse_friends)

    def parse_friends(self, response):
        global id_list
        item = XueqiuItem()
        page_data = json.loads(response.text)
        count = page_data['count']
        page = page_data['page']
        maxPage = page_data['maxPage']
        users = page_data['users']

        for user in users:
            item['id'] = user['id']
            id_list.append(user['id'])
            item['screen_name'] = user['screen_name']
            item['gender'] = user['gender']
            item['city'] = user['city']
            item['province'] = user['province']
            item['verified'] = int(user['verified'])
            item['verified_type'] = user['verified_type']
            item['cube_count'] = user['cube_count']
            item['stocks_count'] = user['stocks_count']

            item['friends_count'] = user['friends_count']
            item['followers_count'] = user['followers_count']
            item['status_count'] = user['status_count']
            item['last_status_id'] = user['last_status_id']
            yield item

        # pop_id = id_list.pop()
        #
        # yield Request(url, callback=parse_friends)

'''
create table User(
   ...> id int primary key,
   ...> screen_name text,
   ...> gender text,
   ...> province text,
   ...> city text,
   ...> verified int,
   ...> verified_type int,
   ...> cube_count int,
   ...> stocks_count int,
   ...> friends_count int,
   ...> followers_count int,
   ...> status_count int,
   ...> last_status_id int,
   ...> is_visited int default 0
   ...> );

# {'city': '阿里',
#  'cube_count': 14,
#  'followers_count': 22043,
#  'friends_count': 68,
#  'gender': 'n',
#  'last_status_id': 84826506,
#  'province': '西藏',
#  'screen_name': '有限次重复博弈',
#  'status_count': 511,
#  'stocks_count': 37,
#  'uid': 1878306520,
#  'verified': False,
#  'verified_type': 0}
sqlite> insert into users
   ...> values(1,1878306520,'有限次重复博弈','n','西藏','阿里',False,0,14,37,68,22043,511,84826506,0);##False 改为0
Error: no such column: False

'''