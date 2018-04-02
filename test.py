from selenium import webdriver  # 导入包
from selenium.webdriver.common.keys import Keys
import time

# browser = webdriver.Chrome()  # 打开Chrome浏览器
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)  # 打开Chrome浏览器
browser.get('http://www.baidu.com')  # 输入url,打开百度首页

input_str = browser.find_element_by_xpath('//*[@id="kw"]')  # 查找输入框
# input_first = browser.find_element_by_id("kw")
# input_second = browser.find_element_by_css_selector("#q")
# input_third = browser.find_element_by_xpath('//*[@id="q"]')

input_str.send_keys("ipad")  # 发送关键字
time.sleep(1)
input_str.clear()  # 清空输入
input_str.send_keys("MakBook pro")  # 发送关键字
button = browser.find_element_by_xpath('//*[@id="su"]')  # 定位按钮
button.click()
print(browser.page_source)
browser.quit()
