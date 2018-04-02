import urllib.request

# 导入urllib.request

f = urllib.request.urlopen('http://www.baidu.com/')
# 打开网址，返回一个类文件对象

print(f.read(500))
# 打印前500字符

print('-------------------------------------------------------')

print(f.read(500).decode('utf-8'))
# 打印前500字符并修改编码为utf-8


import requests  # 导入requests库

r = requests.get('https://www.baidu.com/')
# 使用requests.get方法获取网页信息

print(r.text)
# 打印结果,有乱码

print('-------------------------------------------------------')

r.encoding = 'utf-8'
# 修改编码

print(r.text)
# 打印结果,无乱码
