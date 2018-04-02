'''
【获得数据】，使用 requests.get(url) 或 urllib.request.open(url),返回一个包含网页数据的 response 对象，用 .text 方法转为文本
'''
import requests

# 使用get方法发送请求，返回包含网页数据的Response对象，r.text：返回对象的文本内容
r = requests.get('https://book.douban.com/subject/1084336/comments/').text

'''
【解析数据】，使用 BeautifulSoup4 或 xpath
2.解析网页数据
3.寻找数据
4.for循环打印
'''
from bs4 import BeautifulSoup

soup = BeautifulSoup(r, 'lxml') #传入网页源码，选择lxml 工具解析
pattern = soup.find_all('p', 'comment-content')
for item in pattern:
    print(item.string)

'''
【保存数据】，使用 pandas 保存到本地 或 数据库
1.导入pandas
2.新建list对象
3.使用to_csv写入
'''
import pandas

comments = []
for item in pattern:
    comments.append(item.string)
df = pandas.DataFrame(comments)
df.to_csv("comments.csv")
