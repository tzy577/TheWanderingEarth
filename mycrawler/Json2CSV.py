import json
import csv


def json2csv():

    json_file = open("TWE.json", 'r', encoding='utf8')
    csv_file = open("TWE.csv", 'w', newline='', encoding="utf-8")

    # 读文件
    ls = json.load(json_file)  # 将json格式的字符串转换成python的数据类型，解码过程
    data = [list(ls[0].keys())]  # 获取列名,即key

    for item in ls:
        data.append(list(item.values()))  # 获取每一行的值value

    # 写入文件
    for line in data:
        csv_file.write(",".join(line) + "\n")  # 以逗号分隔一行的每个元素，最后换行 fw.close() #关闭csv文件

    # 关闭文件
    json_file.close()

    csv_file.close()


json2csv()