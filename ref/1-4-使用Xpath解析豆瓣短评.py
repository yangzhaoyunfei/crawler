import requests
from lxml import etree  # 从lxml导入etree(element tree)

url = 'http://www.oasap.com/7-dresses'
htmltext = requests.get(url).text  # 获取 html 数据，使用requests
structure = etree.HTML(htmltext)  # 解析数据，返回 xml 结构,s 代表 structure
print(structure.xpath('//*[@id="ColumnContainer"]/div[1]/a/@href'))  # 使用.xpath()寻找和定位数据，好像都是//开头

url = 'http://www.oasap.com/7-dresses'
htmltext = requests.get(url).text
structure = etree.HTML(htmltext)
# 好像都是//开头，一般返回的是一个数组，用 index 定位需要的元素,要获取所有同级元素，去掉标签后的 index
print(structure.xpath('//div[@class="p_liststyle2"]/a/@title')[0])  # 手写Xpath
#                //*[@id="ColumnContainer"]/div[1]/a

'''
第一种方法：定位到需要爬取的 element 复制Xpath
第二种方法：手写Xpath
获取文本内容用 text()
获取注释用 comment()
获取其它属性用@xx，如：@href,@src,@value
想要获取某个标签下所有的文本（包括子标签下的文本），使用string
如”< p>123< a>来获取我啊< /a>< /p>”，这边如果想要得到的文本为”123来获取我啊”，则需
要使用string
starts-with 匹配字符串前面相等
contains 匹配任何位置相等
'''
