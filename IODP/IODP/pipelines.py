# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class InitPipeline:
    def open_spider(self, spider):
        print('*' * 10 + '开始爬取...' + '*' * 10)


    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        print('*' * 10 + '爬取完毕' + '*' * 10)
