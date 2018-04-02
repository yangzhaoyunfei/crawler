from scrapy.exceptions import DropItem


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()  # 初始化中，创建一个空集合

    def process_item(self, item, spider):
        # 查看id是否在ids_seen中，如果在，就抛弃该Item，如果不在就添加到ids_seen中，下一次其它Item有相同的id就抛弃那个Item,这里只是为了艮验证ID是否重复，不用在集合里放其它属性
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item  # 记住一定要返回Item
