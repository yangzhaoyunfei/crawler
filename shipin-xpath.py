from pyquery import PyQuery as pq
doc = pq(url='http://www.jewelchina.com/a/2018/2018-01-22/139755.html',encoding="utf-8")
print(doc('title'))

