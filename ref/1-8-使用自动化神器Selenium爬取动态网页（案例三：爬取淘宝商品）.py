'''
driver.find_element_by_name()
查找符合条件的单个元素
driver.find_elements_by_name()
查找符合条件的一组元素'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # 预期条件
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as  pq  # 解析工具,也可以用xpath吧
import re
from pymongo import MongoClient

client = MongoClient()
db = client.taobao
haseeset = db.haseenotebook  # 创建神舟笔记本集合
browser = webdriver.Chrome()  # 打开Chrome浏览器
wait = WebDriverWait(browser, 10)  # 等待时间


# 打开淘宝，
def search(kd):
    try:
        browser.get('https://www.taobao.com/')  # 打开url
        input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#q")))  # 定位搜索框
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))  # 定位搜索按钮，见图
        input.send_keys(kd)  # 向搜索框发送关键字
        submit.click()  # 点击搜索按钮
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '#mainsrp-pager > div > div > div > div.total')))  # 获取定位商品列表页的总页数，见页脚图
        get_products()  # 调用下方函数，获取搜索结果第一页商品信息
        print(total.text)
        return total.text
    except TimeoutException:
        return search()  # 超时再次调用


# 跳转到下一页
def next_page(page_number):
    try:
        input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))  # 页码输入框
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()  # 清空页码框
        input.send_keys(page_number)  # 发送目标页码
        submit.click()  # 点击跳转按钮
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'),
            str(page_number)))  # 当前页码
        get_products()  # 获取该页商品信息
    except TimeoutException:
        next_page(page_number)  # 超时再次调用


# 获取某页上的所有商品信息，保存到库里
def get_products():
    products = []
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))  # 等待时间到了以后，定位某搜索结果页下，所有单个商品
    html = browser.page_source  # html源码
    doc = pq(html)  # 应该是返回一个HTML文档对象
    # pyquery （browser.page_source）就相当于requests.get(url)获取的包含网页数据的response对象
    items = doc('#mainsrp-itemlist .items .item').items()  # 获取商品列表中的所有商品
    for item in items:  # 从商品里获取信息，pyquery
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],  # 这里为什么有个index我不清楚
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text(),
        }
        products.append(product)
        print(product)  # 打印单个商品json信息
    haseeset.insert(product)


def main(kd):
    total = search(kd)  # 总爬取页数,第 1 页已在search()中处理
    total = int(re.compile('(\d+)').search(total).group(1))
    for i in range(2, total + 1):  # 从第 2 页开始，爬取所有的数据用total+1
        next_page(i)


if __name__ == '__main__':
    main('神舟笔记本')
