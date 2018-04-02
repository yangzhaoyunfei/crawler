import json


class JsonWriterPipeline(object):
    def open_spider(self, spider):
        # 在爬虫开始时打开文件
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        # 在爬虫结束时关闭文件
        self.file.close()

    def process_item(self, item, spider):
        # 把爬取到的item转换为json格式，保存到文件里
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item  # 注意要返回item
