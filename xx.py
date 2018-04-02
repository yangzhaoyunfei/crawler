from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # 预期条件
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq  # 解析工具,也可以用xpath
import re
from pymongo import MongoClient
import pymysql

# '''mysql'''
# connection = pymysql.connect(host='183.131.202.162', user='root', passwd='Huawei!123', port=3306)
# cursor = connection.cursor()

'''mongo数据库'''
MONGO_URI = 'localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(chrome_options=chrome_options)  # 打开无头Chrome浏览器
browser = webdriver.Chrome()  # 打开Chrome浏览器

wait = WebDriverWait(browser, 10)  # 最长等待时间


# 打开淘宝，
def search(kd):
    try:
        url = 'https://www.taobao.com/'
        browser.get(url)  # 打开url
        '''等待页面元素成功加载出来了，就立即返回相应结果并继续向下执行，否则到了最大等待时间还没有加载出来时，就直接抛出超时异常'''
        '''presence_of_element_located存在并定位元素'''
        input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#q")))  # 定位搜索框
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))  # 定位提交按钮，见图
        input.clear()
        input.send_keys(kd)  # 向搜索框发送关键字
        submit.click()  # 点击提交按钮
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '#mainsrp-pager > div > div > div > div.total')))  # 获取定位商品列表页的总页数，见页脚图
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))  # 等待商品框加载完成
        get_products()  # 调用下方函数，获取搜索结果第一页商品信息
        print('总页数为' + total.text)
        return total.text
    except TimeoutException:
        return search()  # 超时重新调用


#
def next_page(page_number):
    '''
    跳转到下一页
    :param page_number:
    :return:
    '''
    try:
        input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))  # 页码输入框
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()  # 清空页码框
        input.send_keys(page_number)  # 输入目标页码
        submit.click()  # 点击跳转按钮
        '''判断当前高亮的页码数是当前的页码数,防止跳转错误,text_to_be_present_in_element，它会等待指定的文本出现在某一个节点里面时即返回成功'''
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'),
            str(page_number)))  # 当前页码
        get_products()  # 获取该页商品信息
    except TimeoutException:
        next_page(page_number)  # 超时再次调用


def get_products():
    '''
    获取某页上的所有商品信息，保存到库里
    :return:
    '''
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))  # 等待时间到了以后，定位某搜索结果页下，所有单个商品
    html = browser.page_source  # html源码
    doc = pq(html)  # 用HTML文档源代码构造一个PyQuery可解析对象
    items = doc('#mainsrp-itemlist .items .item').items()  # 获取解析对象中的所有商品元素,返回一个列表
    products = []
    for item in items:  # 每个item变量都是一个PyQuery对象
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],  # 这里为什么有个index我不清楚
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text(),
        }
        products.append(product)
        print(product)
        save_to_db(product)
    #     sql = 'insert into taobao(image,price,deal,title,shop,location)values (%s,%s,%s,%s,%s,%s)'
    #
    #     cursor.execute(sql, (
    #         product['image'], product['price'], product['deal'], product['title'], product['shop'],
    #         product['location']))
    # print(products)


def save_to_db(result):
    '''

    :param result:
    :return:
    '''
    try:
        if collection.insert(result):
            pass  # print(result)  # 打印单个商品字典对象
    except Exception:
        print('保存失败！')


def main(kd):
    total = search(kd)  # 总爬取页数,第 1 页已在search()中处理
    total = int(re.compile('(\d+)').search(total).group(1))
    for i in range(2, total + 1):  # 从第 2 页开始，爬取所有的数据用total+1,左闭右开
        next_page(i)
    print('任务完成！')
    browser.close()


if __name__ == '__main__':
    main('神舟笔记本')
