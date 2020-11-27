## 爬取和分析电影《流浪地球》的猫眼评论

项目主要爬取电影《流浪地球》的猫眼和豆瓣评论，把评论保存到mongodb，并且分析该电影出现低分的原因并且使用Django进行展示

主要的文件为：
- ./mycrawler/Crawler_maoyan.py：爬取电影《流浪地球》的猫眼评论的代码（带说明和注释，需要安装MongoDB数据库）
- ./mycrawler/Crawler_douban.py：爬取电影《流浪地球》的豆瓣评论的代码（带说明和注释，需要安装MongoDB数据库）
- ./Data_Analysis/Data_Analysis.ipynb：Jupyter notebook代码，分析该电影的评论和评分
- data.csv: 从MongoDB提取出来的10万条猫眼评论数据
- douban.csv: 从MongoDB提取出来的500条豆瓣评论数据
- stopwords.txt: 停用词表
- Charts_html: 根据数据分析所绘制的图
- ./first/views： Django使用的Views层代码

#### 运行环境：
- python3.8
- 本地MongoDB(MongoDB shell version v3.6.20)数据库

#### 需要安装的包：
-Django==3.1.3
-jieba==0.42.1
-Jinja2==2.11.2
-numpy==1.19.4
-pandas==1.1.4
-pyecharts==1.9.0
-pymongo==3.11.0
-bs4==0.0.1	
-jupyter==1.0.0	
-lxml==4.5.2
-requests==2.25.0	
-fake-useragent==0.1.11	

## Crawling and analysing MaoYan and DouBan comments of The Wandering Earth

This project Crawls MaoYan and DouBan comments of The Wandering Earth, and saves the comments data into MongoDB. It reveals the reason why the movie is getting some bad reputation.
The main files are listed below:
- ./mycrawler/Crawler_maoyan.py：codes for crawling MaoYan comments of The Wandering Earth(with annotation, MOngoDB needs to be installed.)
- ./mycrawler/Crawler_douban.py：codes for crawling DouBan comments of The Wandering Earth(with annotation, MOngoDB needs to be installed.)
./Data_Analysis/Data_Analysis.ipynb：Jupyter notebook for analysing the comments and scores
- data.csv: 100000+ comment MaoYan comments data extracted from MongoDB
- douban.csv: 500 comment DouBan comments data extracted from MongoDB
- stopwords.txt: list of stop words
- Charts_html: diagrams according to the result of data analysis
- ./first/views： code of Django V=Views(MTV)

#### Python environment
- Python3.8
- MongoDB(MongoDB shell version v3.6.20)

#### Packages need to be installed
-Django==3.1.3
-jieba==0.42.1
-Jinja2==2.11.2
-numpy==1.19.4
-pandas==1.1.4
-pyecharts==1.9.0
-pymongo==3.11.0
-bs4==0.0.1	
-jupyter==1.0.0	
-lxml==4.5.2
-requests==2.25.0	
-fake-useragent==0.1.11	

**Notice: If you have any questions, please contact the email tzy577@mail.ustc.edu.cn**
