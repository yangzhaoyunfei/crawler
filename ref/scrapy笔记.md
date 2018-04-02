创建project
scrapy startproject 项目名
cd xxx

创建爬虫
scrapy genspider 爬虫名 example.com（主域名）


启动爬虫(生产环境用)
scrapy crawl 爬虫名

开发环境启动爬虫
用一个文件来启动


css选择器--返回的是一个selectorlist,selector中有element，需要使用extract()去掉selector这个外壳，从而获得element在对元素使用/text(),@href等获取目标信息
    .xx 选择class='xx'的所有元素
     #nn 选择沐='nn'的元素
    p 选择所有<p>元素
    div,p 选择所有<div>和<p>元素
    div p 选择<p>元素,但上层有<div>元素
    div > p 选择<p>元素，但直接父元素为<div>的
    如: sel.css('.xx'), sel.css('#xx'), sel.css('div p')

Xpath选择器--使用[路径表达式]在 XML 文档中选取节点,节点是通过沿着路径或者step来选取的。 一级级下潜的,如:
    sel.xpath(‘/html/body/ul/li’) 严格的文件夹路径形式
    sel.xpath(‘//li’) 查找所有的li标签,而不管层级关系
    sel.xpath(‘//li’)[2].xpath(‘./p’)[0] 查找第三个li标签下的第一个p标签,后一个xpath中的'.'续上了前面的路径,'..'返回上层路径,取元素内的文要用/text(),取元素的属性用@属性名

pyquery选择器--是封装过的css选择器, 已经脱壳,返回的是elmentList,获取元素内容用.text(),取元素属性用.attr('属性名')
    jpy(‘.top’).text() #查找class=‘top’的元素的文本
    jpy(‘.top’).attr(‘class’) #查找class=‘top’的元素的class属性：



查找li标签下所有的文本

items = jpy(‘li’)  #所有<li>元素
for i in items.items():   #遍历
    print(i.text())   #打印元素内的文本
li的div
li的div的div
li的p
li的a的div

查找li标签下所有的class属性

items = jpy(‘li’) #所有<li>元素
for i in items.items():  #遍历
    print(i.attr(‘class’))  #打印元素的属性
top
top
None
None

