import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # 预期条件
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq  # 解析工具,也可以用xpath
import re
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(chrome_options=chrome_options)  # 打开无头Chrome浏览器
browser = webdriver.Chrome()  # 打开Chrome浏览器

wait = WebDriverWait(browser, 10)  # 最长等待时间
url = 'http://www.jewelchina.com/news/news/'
browser.get(url)  # 打开url
'''等待页面元素成功加载出来了，就立即返回相应结果并继续向下执行，否则到了最大等待时间还没有加载出来时，就直接抛出超时异常'''
'''presence_of_element_located存在并定位元素'''
# 栏目列表
# try:
navList = browser.find_elements_by_xpath('/html/body/div[4]/div[2]/a')
for i in range(1, navList.__len__()):
    navList[i].click()
    # 等待加载完成
    # 资讯列表
    newsList = browser.find_elements_by_xpath('/html/body/div[5]/div[1]/ul/li/h2/a')
    for item in newsList:
        time.sleep(3)
        item.click()
        news = {
            'title': browser.find_element_by_xpath("//DT[@class='clearfix']").text,
            'time': browser.find_element_by_xpath("//DL[@class='atitle']/DD[1]").text
        }
        print(news['time'])
        pass

browser.close()
# for item in item
# except Exception:
