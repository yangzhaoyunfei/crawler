import requests
from lxml import etree

url = 'http://www.oasap.com/7-dresses'
htmltext = requests.get(url).text

structure = etree.HTML(htmltext)
data = structure.xpath('//div[@class="p_liststyle2"]/a/@title')

# 使用open函数保存数据
with open('data.txt', 'w', encoding='utf-8') as file:  # 使用with open()新建对象file
    for i in data:
        print(i)
        file.write(i)  # 写入数据，文件保存在当前工作目录

# 使用pandas保存数据
import pandas as pd

df = pd.DataFrame(data)  # 将数据转换为 DataFrame 对象
print(df.head())  # head()只显示前五行，不加则显示全部
df.to_csv('data.csv')
df.to_excel('data.xlsx', sheet_name='Sheet1')  # sheet_name = 'Sheet1' 表示将数据保存在Excel表的第一张表中
print(pd.read_excel('data.xlsx', 'Sheet1', index_col=None, na_values=['NA']))  # 从excel文件中读取数据
