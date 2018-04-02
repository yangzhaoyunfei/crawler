import pymongo


class MongoPipeline(object):
    collection_name = 'scrapy_items'  # 该类的一个属性，非私有

    def __init__(self, mongo_uri, mongo_db):  # 初始化自身的构造函数，构造该类实例时会自动调用该方法对实例进行初始化
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,  # 现在还没有深入理解
                     crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    '''
    Scrapy API的主要入口点是Crawler对象，该对象通过from_crawler(cls, crawler)方法被传递给@classmethod
    def from_crawler(crawler,*args,**kwargs)方法是Scrapy用来生成爬虫的，不必直接重写
    def from_crawler(cls, crawler)方法 # 创建通往crawler的pipeline，返回一个新的pipeline实例，也就是创建一个通住Scrapy API的pipeline,即：pipeline --> crawler --> API
    '''

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
