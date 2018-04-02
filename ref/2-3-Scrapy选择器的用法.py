from scrapy import Selector
from pyquery import PyQuery

with open('index.html', encoding='utf-8') as f:
    html = f.read()
    print(html)
    sel = Selector(text=html)
    jpy = PyQuery(html)
    #xpath
    #re
    pass
