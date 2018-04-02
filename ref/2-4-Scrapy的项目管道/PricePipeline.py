from scrapy.exceptions import DropItem


class PricePipeline(object):
    vat_factor = 1.15

    def process_item(self, item, spider):
        if item['price']:  # 是否有价格
            if item['price_excludes_vat']:  # 如果价格不包括增值税，则把价格乘上一个增值税系数
                item['price'] = item['price'] * self.vat_factor
            return item
        else:  # 如果没有价格，则抛弃这个item
            raise DropItem("Missing price in %s" % item)
