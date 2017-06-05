'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017/5/11
# @Author  : foodish
# @File    : xq_mutlipeople.py
'''
import scrapy
from scrapy.http import Request
from xueqiu.items import XueqiuItem
import json


class XqSpider(scrapy.Spider):
    name = "xueqiu"
    allowed_domains = ["xueqiu.com"]# www.xueqiu.com时报错：offsite
    global visited_id
    visited_id = set()
    # start_id = 1955602780
    start_id = 9442520620
    # user_url = 'https://xueqiu.com/friendships/groups/members.json?page=1&gid=0&uid={uid}'
    friends_url = 'https://xueqiu.com/friendships/groups/members.json?page={page}&gid=0&uid={uid}'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    # cookie = {
    #     'xq_a_token': 'a1e0ac0c42513dcf339ddf01778b49054e341172'
    # }

    cookie = {
        'xq_a_token': 'afe4be3cb5bef00f249343e7c6ad8ac7dc0e17fb'
    }

    def start_requests(self):
        # yield Request(url=self.user_url.format(uid=self.start_id), headers=self.headers, cookies=self.cookie,
        #               callback=self.parse_user)
        global visited_id
        visited_id.add(self.start_id)
        yield Request(url=self.friends_url.format(page=1, uid=self.start_id), headers=self.headers, cookies=self.cookie,
                      callback=self.parse_friends)

    # def parse_user(self, response):
    #     item = XueqiuItem()
    #
    #     for user in json.loads(response.text)['users']:
    #         item['id'] = user['id']
    #         item['screen_name'] = user['screen_name']
    #         item['gender'] = user['gender']
    #         item['city'] = user['city']
    #         item['province'] = user['province']
    #         item['verified'] = int(user['verified'])
    #         item['verified_type'] = user['verified_type']
    #         item['cube_count'] = user['cube_count']
    #         item['stocks_count'] = user['stocks_count']
    #
    #         item['friends_count'] = user['friends_count']
    #         item['followers_count'] = user['followers_count']
    #         item['status_count'] = user['status_count']
    #         item['last_status_id'] = user['last_status_id']
    #         yield item
    #     yield Request(url=self.friends_url.format(page=json.loads(response.text)['page'], uid=response.url.split(
    #         'uid=')[-1]),
    #     headers=self.headers, cookies=self.cookie, callback=self.parse_friends)

    def parse_friends(self, response):
        global visited_id
        item = XueqiuItem()
        page_data = json.loads(response.text)
        count = page_data['count']
        page = page_data['page']
        # print(page)
        maxPage = page_data['maxPage']
        # print(maxPage)
        users = page_data['users']

        friend_list = [user['id'] for user in users]

        uid = response.url.split('uid=')[-1]
        # name_list.add(uid)

        for user in json.loads(response.text)['users']:
            item['id'] = user['id']
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

            item['friendship'] = (uid, user['id'])
            yield item

        visited_id.add(uid)
        # if users:
        #     for user in users:
        #         yield Request(url=self.friends_url.format(page=1, uid=user['id']), headers=self.headers,
        #                       cookies=self.cookie, callback=self.parse_user)
        if page != maxPage:
            next_url = self.friends_url.format(page=str(int(page) + 1), uid=uid)
            print(next_url)
            yield Request(next_url, headers=self.headers, cookies=self.cookie, callback=self.parse_friends)

        if page == maxPage:
            for uid in friend_list:
                if uid not in visited_id:
                    visited_id.add(uid)
                    next_user_url = self.friends_url.format(page=1, uid=uid)
                    print('--------new user------',next_user_url)
                    yield Request(next_user_url, headers=self.headers, cookies=self.cookie, callback=self.parse_friends)


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

