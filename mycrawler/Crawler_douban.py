import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import pymongo
import json
import time


class TWE:
    def __init__(self, page = 0):
        ua = UserAgent()
        self.baseurl = "https://movie.douban.com/subject/26754233/comments?start="
        self.headers ={
            "User-Agent": ua.random,
            "Connnection": "keep-alive",
            "Cookie": "bid=ad7_qlIpexs; douban-fav-remind=1; __yadk_uid=eHymgdIQIa0qS59eOOoAg6bFfc7tSRab; "
                      "_vwo_uuid_v2=DA62ACAA9C640B5D146C68FA029F0E37C|f3e73834809b0c16bf95a85db9d94512; "
                      "push_noty_num=0; push_doumail_num=0; __utmv=30149280.22632; __utmc=30149280; __utmc=223695111; "
                      "loc-last-index-location-id=\"108288\"; ll=\"108288\"; dbcl2=\"226329987:NyLT3UQc1ZU\"; ck=qckA;"
                      " __gads=ID=bcb0a86a756c137d-22312dadb3c400a4:T=1605321966:RT=1605321966:S=ALNI_MYCHXpNA_JZKGQY8Twb3sRlUetuEg; "
                      "__utma=30149280.2014293929.1600301927.1605321946.1605328143.12; "
                      "__utmz=30149280.1605328143.12.6.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/subject/26266893/comments;"
                      " __utmt=1; __utmb=30149280.2.10.1605328143; __utma=223695111.1888304255.1604545180.1605321962.1605328147.11;"
                      " __utmb=223695111.0.10.1605328147; "
                      "__utmz=223695111.1605328147.11.4.utmcsr=search.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/movie/subject_search;"
                      " _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1605328147%2C%22https%3A%2F%2Fsearch.douban.com%2Fmovie%2Fsubject_search%3Fsearch_text%3D%25E5%2585%25AB%25E4%25BD%25B0%26cat%3D1002%22%5D; "
                      "_pk_ses.100001.4cf6=*; _pk_id.100001.4cf6=6391c1e0e9ef2851.1603009738.12.1605328486.1605321967."
        }
        self.info_list = []

        try:
            self.mongo_py = pymongo.MongoClient()
            self.collection = self.mongo_py.The_Eight_Hundred.douban
        except Exception as e:
            print(e)

    def get_response(self, url):
        response = requests.get(url, headers = self.headers)
        data = response.content.decode("utf-8")
        return data

    def parse_usr_url(self, url): # 查看用户详情页存储城市信息

        temp = url.get("href")
        usr_response = requests.get(temp, headers=self.headers).content.decode("utf-8")

        parse_user_data = BeautifulSoup(usr_response, "lxml")

        try:
            user_result = parse_user_data.select(".user-info a")[0].get_text()
        except:
            return "null"
        else:
            return user_result


    def parse_info(self, data):
        parse_data = BeautifulSoup(data, "lxml")

        pattern = re.compile(r'[\u4e00-\u9fa5，。“”：？. a-zA-Z0-9-]+')      # r'[\s]+'
        pattern1 = re.compile('[\S]+')
        pattern2 = re.compile('[\d]+')

        # print(parse_data)

        parse_comment = parse_data.select(".comment-content")
        parse_info = parse_data.select(".comment-info")
        parse_rating = parse_data.select(".rating")
        parse_likes = parse_data.select(".comment-vote")
        parse_url = parse_data.select(".avatar a")

        # for i in range(len(parse_info)):
        #     print(len(parse_info[i]))     # 破解反爬虫的方法

        # print(len(parse_comment), len(parse_info), len(parse_rating))
        # print(parse_rating)
        # print(parse_comment)
        # print(pattern.findall(parse_info))

        j = 0
        for i in range(len(parse_comment)):
            data_dict = {}
            info = pattern.findall(parse_info[i].get_text())
            data_dict["comment"] = parse_comment[i].get_text()
            data_dict["id"] = info[0]
            data_dict["isWatched"] = info[1]
            data_dict["time"] = pattern1.findall(info[2])[0]

            if len(parse_info[i]) != 9:
                data_dict["rating"] = "None"
            else:
                data_dict["rating"] = parse_rating[j].get("title")
                j += 1

            data_dict["likes"] = pattern2.findall(parse_likes[i].get_text())[0]
            data_dict["city"] = self.parse_usr_url(parse_url[i])
            self.info_list.append(data_dict)

            # print(data_dict)
        # print(self.info_list)

    def write_html(self, data_html):
        with open("TWE.html", "w", encoding="utf-8") as f:
            f.write(data_html)
        print("已成功写入html!")

    def write_json(self):
        str_data = json.dumps(self.info_list)
        with open("TWE.json", "w", encoding="utf-8") as f:
            f.write(str_data)

    def save_data2mongo(self):
        with open("TWE.json","r",encoding="utf-8") as f:
            list_ = json.load(f)
        for temp in list_:
            self.collection.insert_one(temp)
        print("已成功写入mongodb")

    # 将评分修改为整数
    def set_rating(self):
        self.collection.update_many({"rating": "力荐"}, {"$set": {"rating": 5}})
        self.collection.update_many({"rating": "推荐"}, {"$set": {"rating": 4}})
        self.collection.update_many({"rating": "还行"}, {"$set": {"rating": 3}})
        self.collection.update_many({"rating": "较差"}, {"$set": {"rating": 2}})
        self.collection.update_many({"rating": "很差"}, {"$set": {"rating": 1}})
        self.collection.update_many({"rating": "None"}, {"$set": {"rating": 3}})

    def run(self):
        for i in range(25):      # 只能爬取500条数据（前24页）
            url = self.baseurl + str(i * 20) + "&limit=20&status=P&sort=new_score"
            request = self.get_response(url)
            # self.write_html(request)
            self.parse_info(request)
            print("爬取第" + str(i) + "页成功！")
            # time.sleep(1)

        self.write_json()
        print("写入json成功！")
        self.save_data2mongo()
        print("写入Mongodb成功！")
        self.set_rating()


if __name__ == '__main__':
    my = TWE()
    my.run()
