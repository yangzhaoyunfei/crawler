'''爬取网页通用框架
定义函数
设置超时
异常处理
调用函数'''

import requests  # 导入Requests库


# 定义函数
def getHtmlText(url):
    try:
        r = requests.get(url, timeout=20)  # 设置超时
        print('响应状态：', r.status_code)  # 打印状态码
        r.raise_for_statu()  # 抛出异常
        r.encoding = r.apparent_encoding
        return r.text
    except:  # 异常处理
        return '产生异常'


# 在这里填入
if __name__ == "__main__":
    url = 'https://www.zhihu.com/'
    print(getHtmlText(url))  # 调用函数url

'''
爬虫协议https://www.baidu.com/robots.txt
拦截所有的机器人：
User-agent: *
Disallow: /
允许所有的机器人：
User-agent: *
Disallow:
'''
