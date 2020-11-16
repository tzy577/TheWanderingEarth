import os
import time
import requests
import pymongo
from fake_useragent import UserAgent
import random

class MaoYan(object):
    """
    猫眼评论爬虫，爬取电影《流浪地球》的评论和评分
    """

    def __init__(self):
        """
        初始化函数
        :param
        headers: 请求头
        """

        ua = UserAgent()

        self.headers = {
            'User-Agent': ua.random,
            'Connection': 'keep-alive',
            'Cookie': "__mta=245808059.1605353499202.1605353564879.1605353567063.4; uuid_n_v=v1; "
                      "uuid=F494AD80266C11EBA6D265B8A52522AFC517213E1EC54DE1B9C9EC0FA5AA808F;"
                      " _csrf=0991efc1cf790ad4fb6b8d814be2a00314ea479cbec04a377826f7ae73a737f0; "
                      "_lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=175c68669b8c8-0adb8e124fa581-3e604902-1fa400-175c68669b9c8;"
                      " _lxsdk=F494AD80266C11EBA6D265B8A52522AFC517213E1EC54DE1B9C9EC0FA5AA808F; "
                      "lt=dBFFUmiMHoPs6Cwd0TidBHT-sbsAAAAABgwAABUWjs4bFbZNH8JdVOvdxYPkrRCJ8s_EbhXPNMo2o14BQEoTa1atD9gSPM-3Yaobqw;"
                      " lt.sig=TB1-SN6Aw-abY4nSDkYcIPViFlM; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1605353499,1605353554;"
                      " __mta=245808059.1605353499202.1605353553816.1605353564879.3; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1605353567;"
                      " _lxsdk_s=175c68669ba-68a-86d-cb1%7C%7C10"
            }

        # 配置mongodb数据库
        # host = os.environ.get('MONGODB_HOST', '127.0.0.1')  # 本地数据库
        # port = os.environ.get('MONGODB_PORT', '27017')  # 数据库端口
        # mongo_url = 'mongodb://{}:{}'.format(host, port)
        # mongo_db = os.environ.get('MONGODB_DATABASE', 'The_Wandering_Earth')
        # client = MongoClient(mongo_url)
        # self.db = client[mongo_db]
        # # self.db['maoyan'].create_index('id', unique=True)  # 以评论的id为主键进行去重

        try:
            self.mongo_py = pymongo.MongoClient()
            self.collection = self.mongo_py.The_Wandering_Earth.maoyan
        except Exception as e:
            print(e)

    def get_comment(self):
        """
        爬取首映到当前时间的电影评论
        :param
        url: 评论真实请求的url，参数ts为时间戳
        :return: None
        """
        proxies = [
            {"HTTP": "117.64.224.210:1133"},
            {"HTTP": "144.255.48.172:9999"},
            {"HTTP": "182.34.22.143:9999"},
            {"HTTP": "175.42.122.206:9999"},
            {"HTTP": "123.55.114.70:9999"},
            {"HTTP": "123.54.40.139:9999"},
            {"HTTP": "1.199.31.14:9999"},
            {"HTTP": "115.221.240.118:9999"},
            {"HTTP": "171.11.29.23:9999"},
            {"HTTP": "113.121.36.148:9999"}
        ]

        url = "https://m.maoyan.com/review/v2/comments.json?movieId=248906&userId=-1&offset={}&limit=15&type=3"
        for i in range(250, 1001):
            proxy = random.choice(proxies)
            req_url = url.format(i)
            res = requests.get(req_url, headers=self.headers, proxies=proxy).json()['data']['comments']
            for com in res:
                self.parse_comment(com)

            print('成功爬取到第{}页的数据！'.format(i))
            time.sleep(1)

    def parse_comment(self, com):
        """
        解析函数，用来解析爬回来的json评论数据，并把数据保存进mongodb数据库
        :param com: 每一条评论的json数据
        :return:
        """
        comment = {'content': com['content'], 'gender': com['gender'], 'id': com['id'],
                   'nick': com['nick'], 'replyCount': com['replyCount'], 'score': com['score'],
                   'time': com['time'], 'upCount': com['upCount'],
                   'userId': com['userId'], 'userLevel': com['userLevel']}  # 构造评论字典
        # 通过评论id去重，如果已经有了就更新，没有就插入
        # temp = self.db['maoyan'].update_one({"id": com["id"]}, {"$set": comment})
        # if temp == 0:
        self.collection.insert_one(comment)




if __name__ == '__main__':
    my = MaoYan()
    my.get_comment()
