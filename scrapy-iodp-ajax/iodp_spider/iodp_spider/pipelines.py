# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import requests
from .spiders.header_params import *


def save_header(report, exception):
    """
    写入文件中表的header
    """
    dictionary = dict(requests.get(url=header_url.format(report)).json())
    header = None
    if 'headers' in dictionary:
        header = dictionary['headers']
    else:
        return
    with open('./CSV/' + report + '_' + exception + '.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        print(report + '_' + exception + '.csv', '文件头', '写入成功')
        f.close()


class IodpSpiderPipeline:
    def process_item(self, item, spider):
        print(item['report'] + '_' + item['exception'] + '.csv', '正在写入...')
        with open('./CSV/' + item['report'] + '_' + item['exception'] + '.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(item['data_text'])
            print('写入成功!!!')
            f.close()

        return item
