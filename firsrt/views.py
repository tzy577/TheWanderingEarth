
# Django使用的包
from django.shortcuts import render
from django.http import HttpResponse

# 数据分析使用的包
import pandas as pd
import numpy as np

# 文本语义分析使用的包
from collections import Counter
import jieba        # jieba最好使用vpn下载，或者换源

# 可视化使用的pyecharts
from pyecharts.globals import CurrentConfig
from pyecharts.charts import Bar, Grid, Line, Page, Map, Pie, Scatter, Liquid, Tab, WordCloud
from pyecharts import options as opts
from pyecharts.components import Table
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from pyecharts.globals import SymbolType

# 数据库使用的是pymongo
from pymongo import MongoClient

# 数据清洗需要使用正则表达式
import re
from jinja2 import Environment, FileSystemLoader

# Create your views here.
# def index(reqeust):
#     return render(reqeust, 'index.html')

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./first/templates"))

# 连接数据库
conn = MongoClient(host='127.0.0.1', port=27017)  # 实例化MongoClient
db = conn.get_database('The_Wandering_Earth')  # 连接到TWH1数据库

# 猫眼数据以及保存为data.csv文件，无需从数据库中导出

douban = db.get_collection('douban') # 连接到集合comment
# maoyan = db.get_collection("maoyan")
douban_data = douban.find()
# maoyan_data = maoyan.find()

# 读取数据
data1 = pd.json_normalize([comment for comment in douban_data])
data2 = pd.read_csv("data.csv")


# 数据清洗
data1 = data1.drop(columns= "_id")
data1 = data1.drop(columns= "isWatched")
data1['time'] = pd.to_datetime(data1['time'], format='%Y-%m-%d')
data1 = data1[data1['time']>=pd.to_datetime('2019-02-01 00:00:00')]
data1.set_index(data1["time"], inplace=True)

print("\n")

data2 = data2.drop(columns='id')
data2 = data2.drop_duplicates(subset='userId')
data2['time'] = pd.to_datetime(data2['time'])

# 若使用数据库打开数据，数据时间字段的清洗用下面语句，将上一条语句注释
# data2['time'] = pd.to_datetime(data2['time']/1000, unit='s')

data2 = data2[data2['time']>=pd.to_datetime('2019-02-01 00:00:00')]
data2.set_index(data2["time"], inplace=True)


# 将评分数据转换为python中的int类型
# 豆瓣：力荐=5，推荐=4，还行=3，较差=2，很差=1
# 猫眼：力荐=9-10，推荐=7-8，还行=5-6，较差=2-4，很差=1-0
rating_str = ["很差", "较差", "还行", "推荐", "力荐"]
rating_score1 = []
rating_score2 = [0,0,0,0,0]

# print(pd.value_counts(data1["rating"].values))

for i in range(1,6):
    rating_score1.append(pd.value_counts(data1["rating"].values)[i])

# print(pd.value_counts(data2["score"]))
for key,value in pd.value_counts(data2["score"]).items():
    # print(key,value)
    if key == 10 or key ==9:
        rating_score2[4] += value
    if key == 8 or key ==7:
        rating_score2[3] += value
    if key == 6 or key ==5:
        rating_score2[2] += value
    if key == 4 or key ==3:
        rating_score2[1] += value
    if key == 2 or key ==1:
        rating_score2[0] += value


#[['很差', 43], ['较差', 55], ['还行', 172], ['推荐', 128], ['力荐', 102]]
list_1 = [list(z) for z in zip(rating_str, rating_score1)]
list_2 = [list(z) for z in zip(rating_str, rating_score2)]


# 展示豆瓣中评分饼图
def Rating_Pie():
    c1 = (
        Pie()
        .add(
            "",
            [['很差', 43], ['较差', 55], ['还行', 172], ['推荐', 128], ['力荐', 102]],
            center=["30%", "45%"],
            radius=[60, 80],
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
        .add(
            "",
            list_2,
            center=["65%", "45%"],
            radius=[60, 80],
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="评分饼图"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

    )

    return c1


def Rating_line_bar():
    list_ = [43, 55, 172, 128, 102]
    # 展示豆瓣中评分折线图
    bar = (
        Bar()
        .add_xaxis(rating_str)
        .add_yaxis("豆瓣", list_)
        .add_yaxis("猫眼", rating_score2)
        .set_global_opts(title_opts=opts.TitleOpts(title="评分分布柱状图"))
    )
    line = (
        Line()
        .add_xaxis(rating_str)
        .add_yaxis("豆瓣", list_)
        .add_yaxis("猫眼", rating_score2)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="评分分布折线图", pos_top="48%"),
            legend_opts=opts.LegendOpts(pos_top="48%"),
        )
    )

    grid = (
        Grid()
        .add(bar, grid_opts=opts.GridOpts(pos_bottom="60%"))
        .add(line, grid_opts=opts.GridOpts(pos_top="60%"))
    )

    return grid

# 从猫眼和豆瓣的评分中按照每天求平均值
score_by_time1 = data1['rating'].resample('D').mean()
score_by_time2 = data2['score'].resample('D').mean()


# 分别存储猫眼豆瓣日期（精确到天）和对应每天得分的平均值
douban_time = []
douban_score = []
for time,score in score_by_time1.items():
    douban_time.append(time)
    douban_score.append(round(score,2))     # 为每天的平均得分保留两位小数


maoyan_time = []
maoyan_score = []
for time,score in score_by_time2.items():
    maoyan_time.append(time)
    maoyan_score.append(round(score,2))


def Score_by_time_maoyan():
    c1 = (
        Bar()
        .add_xaxis(maoyan_time)
        .add_yaxis("猫眼评论", maoyan_score)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="猫眼评分随时间变化图"),
            datazoom_opts=[opts.DataZoomOpts()],
        )
    )
    return c1


def Score_by_time_douban():
    c2 = (
        Bar()
        .add_xaxis(douban_time)
        .add_yaxis("豆瓣评论", douban_score)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="豆瓣评分随时间变化图"),
            datazoom_opts=[opts.DataZoomOpts()],
        )
    )
    return c2


# 设置省份正则表达式用于获取豆瓣评论人的所属省份（去除省以下行政划分）
pattern = re.compile('[湖南|湖北|广东|广西|河南|河北|山东|山西|江苏|浙江|江西|黑龙江|'
                     '新疆|云南|贵州|福建|吉林|安徽四川|西藏|宁夏|辽宁|青海|'
                     '甘肃|陕西|内蒙古||台湾|北京|上海|天津]+')

info = data1['city'].value_counts()
province = info.keys()
amount = info.values

result = []

provinces = ['湖南', '湖北', '广东', '广西', '河南', '河北', '山东', '山西', '江苏', '浙江', '江西', '黑龙江', '新疆', '云南', '贵州', '福建', '吉林', '安徽', '四川', '西藏', '宁夏', '辽宁', '青海', '甘肃', '陕西', '内蒙古', '台湾', '北京', '上海', '天津']
temp_amount = []
temp_province = []

# 以下循环用于获得个人简介中填写的省份
for i in range(len(province)):
    if pattern.findall(province[i]) != []:
        if pattern.findall(province[i])[0][:2] in temp_province:
            index = temp_province.index(pattern.findall(province[i])[0][:2])
            temp_amount[index] += int(amount[i])
        else:
            temp_province.append(pattern.findall(province[i])[0][:2])
            temp_amount.append(int(amount[i]))
        # result.append(temp)

result = [list(z) for z in zip(temp_province, temp_amount)]

# 绘制每个省份的评论人数
def Map_amount():
    c = (
        Map()
        .add("评论人数", result, "china")
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=150, is_piecewise=True),
            title_opts=opts.TitleOpts(title="评论人数分布图"),
        )
    )

    return c

# 得到豆瓣数据中的评分和点赞数字段
rating = data1['rating'].values
likes = data1['likes'].values
likes_new = [0, 0, 0, 0, 0]
sum = 0


# 按评分统计点赞人数
for i in range(len(rating)):
    if int(rating[i]) == 1:
        likes_new[0] += int(likes[i])
    elif int(rating[i]) == 2:
        likes_new[1] += int(likes[i])
    elif int(rating[i]) == 3:
        likes_new[2] += int(likes[i])
    elif int(rating[i]) == 4:
        likes_new[3] += int(likes[i])
    else:
        likes_new[4] += int(likes[i])

# 统计点赞总人数
for j in range(len(likes_new)):
    sum += likes_new[j]

# 设置高分为4和5分，低分为1和2分，计算相应的好评率和差评率
favorate_rate = (likes_new[3] + likes_new[4]) / sum
poor_rate = (likes_new[0] + likes_new[1]) / sum
# print(type(favorate_rate), type(poor_rate))

# print(likes_new)

# 绘制评分-点赞散点图
def scatter_rating_likes() -> Scatter:
    c = (
        Scatter()
        .add_xaxis(range(1,6))
        .add_yaxis("点赞数", likes_new)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="评分-点赞图"),
            visualmap_opts=opts.VisualMapOpts(type_="size", max_=100000, min_=20000),
        )
    )
    return c

# 绘制球形液体图展示好评率和差评率
def grid_liquid_favorate_rate() -> Grid:
    l1 = (
        Liquid().
        add(
        "好评率",
        [favorate_rate],
        center=["60%", "50%"],
        label_opts=opts.LabelOpts(
            font_size=50,
            formatter=JsCode(
                """function (param) {
                        return (Math.floor(param.value * 10000) / 100) + '%';
                    }"""
             ),
            position="inside",
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="好评率和差评率"))
    )

    l2 = (
        Liquid().
        add(
        "差评率",
        [poor_rate],
        center=["25%", "50%"],
        label_opts=opts.LabelOpts(
            font_size=50,
            formatter=JsCode(
                """function (param) {
                        return (Math.floor(param.value * 10000) / 100) + '%';
                    }"""
             ),
            position="inside",
            ),
        )
    )

    grid = Grid().add(l2, grid_opts=opts.GridOpts()).add(l1, grid_opts=opts.GridOpts())
    return grid


# 文本情感分析：

# 将流浪地球演员名字加入jieba
jieba.add_word('屈楚萧')
jieba.add_word('刘启')
jieba.add_word('吴京')
jieba.add_word('刘培强')
jieba.add_word('李光洁')
jieba.add_word('王磊')
jieba.add_word('吴孟达')
jieba.add_word('达叔')
jieba.add_word('韩子昂')
jieba.add_word('赵今麦')
jieba.add_word('韩朵朵')

# 获得常用句尾词
swords = [x.strip() for x in open ('stopwords.txt', encoding="utf-8")]

# 因为猫眼数据将时间作为了索引，而绘制词云不需要时间信息，因此设置正则表达式获得非数字的信息
pattern = re.compile('[^\d]+')

def plot_word_cloud_maoyan(data, swords, path):

    text = ''
    # 将所有评论连接起来，以便于jieba切分词语
    for temp_i in data['content']:
        text += str(temp_i)

    words = list(jieba.cut(text))
    ex_sw_words = []
    for word in words:
        if len(word)>1 and (word not in swords):
            ex_sw_words.append(word)
    c = Counter()
    c = Counter(ex_sw_words)
    # 计算所有评论中词语的出现频率
    wc_data = pd.DataFrame({'word':list(c.keys()), 'counts':list(c.values())}).sort_values(by='counts', ascending=False).head(100)
    # print(wc_data)

    # 绘制猫眼对应的高分和低分词云
    c = (
    WordCloud()
    .add("", wc_data.values, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
    .set_global_opts(title_opts=opts.TitleOpts(title=path))
    )

    return c

    # 绘制豆瓣对应的高分和低分词云
def plot_word_cloud_douban(data, swords, path):
    # 豆瓣的评论没有设置时间索引，可以直接连接
    text = ''.join(data['comment'])
    words = list(jieba.cut(text))
    ex_sw_words = []
    for word in words:
        if len(word)>1 and (word not in swords):
            ex_sw_words.append(word)
    c = Counter()
    c = Counter(ex_sw_words)
    wc_data = pd.DataFrame({'word':list(c.keys()), 'counts':list(c.values())}).sort_values(by='counts', ascending=False).head(100)
    print(wc_data)

    c = (
    WordCloud()
    .add("", wc_data.values, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
    .set_global_opts(title_opts=opts.TitleOpts(title=path))
    )

    return c


# 绘制豆瓣的评价的词云
# 高分
def WordCloud_douban_high():
    c = plot_word_cloud_douban(data=data1[data1['rating']>=4], swords=swords, path="豆瓣高分评论词云")
    return c
# 低分
def WordCloud_douban_low():
    c = plot_word_cloud_douban(data=data1[data1['rating']<=2], swords=swords, path="豆瓣低分评论词云")
    return c



# 绘制猫眼的评价的词云
def WordCloud_maoyan_high():
# 高分
    c = plot_word_cloud_maoyan(data=data2[data2['score']>7], swords=swords, path="猫眼高分评论词云")
    return c
# 低分
def WordCloud_maoyan_low():
    c = plot_word_cloud_maoyan(data=data2[data2['score']<4], swords=swords, path="猫眼低分评论词云")
    return c

# 将词云放在可以分页的图中,无法使用。
def Tab_WordCloud():
    tab = Tab()
    tab.add(WordCloud_douban_high(), "豆瓣高分词云")
    tab.add(WordCloud_douban_low(), "豆瓣低分词云")
    tab.add(WordCloud_maoyan_high(), "猫眼高分词云")
    tab.add(WordCloud_maoyan_low(), "猫眼低分词云")

    return tab


# 评分的人群有哪些特征？（性别、等级）

# 1). 评分和性别及等级的关系(都只有在猫眼的数据中才有对应的字段)

# 评分和性别的关系
# 0代表未知，1代表男，2代表女

# 获得总体各个性别的个数
gender_total_maoyan = data2['gender'].value_counts().values
# print(gender_total_maoyan.values)

# 获得低分各个性别的个数
gender_low_maoyan = data2.loc[data2['score']<4, 'gender'].value_counts().values

# 获得低分各个性别的个数
gender_high_maoyan = data2.loc[data2['score']>7, 'gender'].value_counts().values

# print(data2['gender'].value_counts())

# 将对应性别个数转换为int类型
total_sex = []
for i in gender_total_maoyan:
    total_sex.append(int(i))

# 将低分对应性别个数转换为int类型
low_sex = []
for j in gender_low_maoyan:
    low_sex.append(int(j))
# 数据库中猫眼低分评论只有3条，2条没有说明性别，1条为男性,因此添加女性数为0
# low_sex.append(0)

# 将高分对应性别个数转换为int类型
high_sex = []
for k in gender_high_maoyan:
    high_sex.append(int(k))

sum1 = total_sex[1] + total_sex[2]
sum2 = high_sex[1] + high_sex[2]
sum3 = low_sex[1] + low_sex[2]

# 将未知人数去掉并且求得每一种男女所占比例
total_sex_per = [round(total_sex[1]/sum1 * 100, 2), round(total_sex[2]/sum1 * 100, 2)]
high_sex_per = [round(high_sex[1]/sum2 * 100, 2), round(high_sex[2]/sum2 * 100, 2)]
low_sex_per = [round(low_sex[1]/sum3 * 100, 2), round(low_sex[2]/sum3 * 100, 2)]



# 评分和等级的关系

# 获得总体各个等级的个数
level_total_maoyan = data2['userLevel'].value_counts().sort_index().values
# print(gender_total_maoyan.values)

# 获得低分各个等级的个数
level_low_maoyan = data2.loc[data2['score']<4, 'userLevel'].value_counts().sort_index().values

# 获得高分各个等级的个数
level_high_maoyan = data2.loc[data2['score']>7, 'userLevel'].value_counts().sort_index().values

# 用于查看用户等级和人数
# print(data2['userLevel'].value_counts().sort_index())
# print(data2.loc[data2['score']<4, 'userLevel'].value_counts().sort_index())
# print(data2.loc[data2['score']>7, 'userLevel'].value_counts().sort_index())
# print(level_high_maoyan,level_low_maoyan,level_total_maoyan)

# 将对应等级个数转换为int类型
total_level = []
for i in level_total_maoyan:
    total_level.append(int(i))

# 将低分对应等级个数转换为int类型
low_level = []
for j in level_low_maoyan:
    low_level.append(int(j))
# 数据库中猫眼低分评论没有1，3，4级的用户,因此令对应等级的人数为0


# 将高分对应等级个数转换为int类型
high_level = []
for k in level_high_maoyan:
    high_level.append(int(k))

sum1 = 0
sum2 = 0
sum3 = 0

# 计算总体，高分，低分不同等级的总人数
for i in range(len(total_level)):
    sum1 += total_level[i]
    sum2 += high_level[i]
    sum3 += low_level[i]

total_level_per = []
high_level_per = []
low_level_per = []

# 求各个等级的所占比例
for i in range(len(total_level)):

    total_level_per.append(round(total_level[i]/sum1 * 100, 2))
    high_level_per.append(round(high_level[i]/sum2 * 100, 2))
    low_level_per.append(round(low_level[i]/sum3 * 100, 2))

# 绘制《流浪地球》观众性别，等级条形图和饼图

# 绘制性别分布条形图
def sex_distribution_bar() -> Bar:
    bar = (
        Bar()
        .add_xaxis(['未知', '男', '女'])
        .add_yaxis("总体性别分布", total_sex)
        .add_yaxis("高分性别分布", high_sex)
        .add_yaxis("低分性别分布", low_sex)
        .set_global_opts(title_opts=opts.TitleOpts(title="观众性别分布条形图"))
    )
    return bar

# 绘制性别分布饼图
def sex_distribution_pie() -> Pie:
    fn = """
        function(params) {
            if(params.name == '女')
                return '\\n\\n\\n' + params.name + ' : ' + params.value + '%';
            return params.name + ' : ' + params.value + '%';
        }
        """

    def new_label_opts():
        return opts.LabelOpts(formatter=JsCode(fn), position="center")

    pie = (
        Pie()
        .add(
            "",
            [list(z) for z in zip(['男', '女'], total_sex_per)],
            center=["15%", "30%"],
            radius=[60, 80],
            label_opts=new_label_opts(),
        )
        .add(
            "",
            [list(z) for z in zip(['男', '女'], high_sex_per)],
            center=["40%", "30%"],
            radius=[60, 80],
            label_opts=new_label_opts(),
        )
        .add(
            "",
            [list(z) for z in zip(['男', '女'], low_sex_per)],        #没有女性特殊处理
            center=["65%", "30%"],
            radius=[60, 80],
            label_opts=new_label_opts(),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="观众性别分布饼图"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="80%", orient="vertical"
            ),
        )
    )

    return pie

# 查看数据格式
# print([list(z) for z in zip(['男', '女'], low_sex_per)])
# print([list(z) for z in zip(['0', '1', '2', '3', '4', '5', '6'], total_level_per)])

# 绘制等级分布条形图
def level_distribution_bar() -> Bar:
    bar = (
        Bar()
        .add_xaxis([0, 1, 2, 3, 4, 5, 6])
        .add_yaxis("总体等级分布", total_level)
        .add_yaxis("高分等级分布", high_level)
        .add_yaxis("低分等级分布", low_level)
        .set_global_opts(title_opts=opts.TitleOpts(title="观众等级分布条形图"))
    )
    return bar

# 绘制等级分布饼图
def level_distribution_pie() -> Pie:
    fn = """
        function(params) {
            if(params.name == '5')
                return '\\n\\n\\n\\n\\n\\n\\n\\n\\n' + params.name + ' : ' + params.value + '%';
            if(params.name == '4')
                return '\\n\\n\\n\\n\\n\\n\\n' + params.name + ' : ' + params.value + '%';
            if(params.name == '3')
                return '\\n\\n\\n\\n\\n' + params.name + ' : ' + params.value + '%';
            if(params.name == '2')
                return '\\n\\n\\n' + params.name + ' : ' + params.value + '%';
            if(params.name == '1')
                return '\\n' + params.name + ' : ' + params.value + '%';
            if(params.name == '0' || params.name == '6')
                return ' ';

        }
        """

    def new_label_opts():
        return opts.LabelOpts(formatter=JsCode(fn), position="center")

    # 绘制饼图的时候1，2，3，4类型要是字符串类型
    pie = (
        Pie()
        .add(
            "",
            [list(z) for z in zip(['0', '1', '2', '3', '4', '5', '6'], total_level_per)],
            center=["15%", "30%"],
            radius=[80, 100],
            label_opts=new_label_opts(),
        )
        .add(
            "",
            [list(z) for z in zip(['0', '1', '2', '3', '4', '5', '6'], high_level_per)],
            center=["40%", "30%"],
            radius=[80, 100],
            label_opts=new_label_opts(),
        )
        .add(
            "",
            [list(z) for z in zip(['0', '1', '2', '3', '4', '5', '6'], low_level_per)],        #没有女性特殊处理
            center=["65%", "30%"],
            radius=[80, 100],
            label_opts=new_label_opts(),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="观众等级分布饼图"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="80%", orient="vertical"
            ),
        )
    )

    return pie

# page类型的页面无法展示
# 将条形图和饼图放在一起展示
def page_layout1() -> Page:
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        sex_distribution_bar(),
        sex_distribution_pie()

    )
    return page


def page_layout2() -> Page:
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        level_distribution_bar(),
        level_distribution_pie()

    )
    return page


# 高低分跟哪位演员有关？

# 将演员真名，真名绰号，角色绰号和电影角色名做一个映射
mapping = {'liucixin':'刘慈欣|大刘', 'guofan':'郭帆', 'quchuxiao':'屈楚萧|刘启|户口|男主', 'wujing':'吴京|刘培强|战狼',
           'liguangjie':'李光洁|王磊', 'wumengda':'吴孟达|达叔|韩子昂', 'zhaojinmai':'赵今麦|韩朵朵|女主'}

# 将演员名字的拼音作为数据的新字段，若该条记录出现了该演员，则将其名字的拼音对应为true
for key, value in mapping.items():
    data2[key] = data2['content'].str.contains(value)

# 将对应的人名拼音和在数据中的出现次数形成字典

# 求所有评论中出现的演员名及其个数
# 因为数据存在Nah值，无法处理，因此pd.Series({key: data.loc[data[key], 'score']无法使用，但是使用分数≥0也可以做到相同效果
staff_count = pd.Series(
    {key: data2.loc[data2[key] & (data2['score'] >= 0), 'score'].count() for key in mapping.keys()}).sort_index()

# 求高分评论中出现的演员名及其个数
staff_count_high = pd.Series({key: data2.loc[data2[key]&(data2['score']>7), 'score'].count() for key in mapping.keys()}).sort_index()

# 求低分评论中出现的演员名及其个数
staff_count_low = pd.Series({key: data2.loc[data2[key]&(data2['score']<4), 'score'].count() for key in mapping.keys()}).sort_index()

# 演员在低分评论的提及次数 占 所有评论中该演员的提及次数
staff_count_pct1 = np.round(staff_count_low/staff_count*100, 2).sort_index()

# 演员在高分评论的提及次数 占 所有评论中该演员的提及次数
staff_count_pct2 = np.round(staff_count_high/staff_count*100, 2).sort_index()

# 绘制演员在低分/高分评论的提及次数 占 所有评论中该演员的提及次数的柱状图

# 所有演员以下列顺序出现
# ['guofan', 'liguangjie', 'liucixin', 'quchuxiao', 'wujing', 'wumengda','zhaojinmai']

# 存放演员的总出现次数
count1 = []
# 存放好评中演员的总出现次数
count2 = []
# 存放差评中演员的总出现次数
count3 = []

for i in range(len(staff_count)):
    count1.append(int(staff_count[i]))
    count2.append(int(staff_count_high[i]))
    count3.append(int(staff_count_low[i]))

# print(count1,count2,count3)
list1 = []
list2 = []
list3 = []

# 将数据转换为指定的数据格式（整型int）
for i in range(len(staff_count)):
    temp1 = {}
    temp2 = {}
    temp3 = {}

    temp1["value"] = count2[i]
    temp1["percent"] = count2[i] / count1[i]
    list1.append(temp1)
    temp2["value"] = count3[i]
    temp2["percent"] = count3[i] / count1[i]
    list2.append(temp2)
    temp3["value"] = (count1[i] - count2[i] - count3[i])
    temp3["percent"] = (count1[i] - count2[i] - count3[i]) / count1[i]
    list3.append(temp3)


# 主要演员高分评论转换为整型
rows_h1 = []
rows_h2 = []
rows_h3 = []
rows_h4 = []
for i in range(5):
    comment1 = [data2[data2['wumengda']&(data2['score']>7)].nlargest(5, 'upCount').values[i][0]]
    comment2 = [data2[data2['wujing']&(data2['score']>7)].nlargest(5, 'upCount').values[i][0]]
    comment3 = [data2[data2['zhaojinmai']&(data2['score']>7)].nlargest(5, 'upCount').values[i][0]]
    comment4 = [data2[data2['quchuxiao']&(data2['score']>7)].nlargest(5, 'upCount').values[i][0]]
    rows_h1.append(comment1)
    rows_h2.append(comment2)
    rows_h3.append(comment3)
    rows_h4.append(comment4)

# 主要演员低分评论转换为整型
rows_l1 = []
rows_l2 = []
rows_l3 = []
rows_l4 = []
for i in range(5):
    comment1 = [data2[data2['wumengda']&(data2['score']<4)].nlargest(5, 'upCount').values[i][0]]
    comment2 = [data2[data2['wujing']&(data2['score']<4)].nlargest(5, 'upCount').values[i][0]]
    comment3 = [data2[data2['zhaojinmai']&(data2['score']<4)].nlargest(5, 'upCount').values[i][0]]
    comment4 = [data2[data2['quchuxiao']&(data2['score']<4)].nlargest(5, 'upCount').values[i][0]]
    rows_l1.append(comment1)
    rows_l2.append(comment2)
    rows_l3.append(comment3)
    rows_l4.append(comment4)

def Evaluate_bar():
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(['郭帆', '李光洁', '刘慈欣', '屈楚萧', '吴京', '吴孟达', '赵今麦'])
            .add_yaxis("好评提及次数", list1, stack="stack1", category_gap="50%")
            .add_yaxis("差评提及次数", list2, stack="stack1", category_gap="50%")
            .add_yaxis("中评提及次数", list3, stack="stack1", category_gap="50%")
            .set_series_opts(
            label_opts=opts.LabelOpts(
                position="right",
                formatter=JsCode(
                    "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
                ),
            )
        )
    )

    return c



# 总体布局绘制的可视化图
def Page_Layout(request):
    page = Page(layout=Page.DraggablePageLayout)
    page.add(
        Rating_Pie(),
        Rating_line_bar(),
        Score_by_time_douban(),
        Score_by_time_maoyan(),
        Map_amount(),
        scatter_rating_likes(),
        grid_liquid_favorate_rate(),
        WordCloud_douban_high(),
        WordCloud_douban_low(),
        WordCloud_maoyan_high(),
        WordCloud_maoyan_low(),
        sex_distribution_bar(),
        sex_distribution_pie(),
        level_distribution_bar(),
        level_distribution_pie(),
        Evaluate_bar()

    )
    return HttpResponse(page.render_embed())