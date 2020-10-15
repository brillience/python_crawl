# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import re

# useful for handling different item types with a single interface
from scrapy import Request
from scrapy.pipelines.files import FilesPipeline
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# class initPipeline:
#     def open_spider(self, spider):
#         print('*' * 10 + '开始下载...' + '*' * 10)
#         options = Options()
#         options.add_argument('--headless')
#         options.add_argument('--disable_gpu')
#         self.chrome = webdriver.Chrome(chrome_options=options)

#     def process_item(self, item, spider):
#         return item

#     def close_spider(self, spider):
#         print('*' * 10 + '爬取完毕' + '*' * 10)
#         self.chrome.quit()

class fileDown(FilesPipeline):
    def get_media_requests(self, item, info):
        # 向FilesPipline提交url地址，进行文件下载
        for url in item['file_urls']:
            yield Request(url)

    def file_path(self, request, response=None, info=None):
        # 设置保存的文件名
        find_name = re.compile(r"/(.*?)?download=true")
        file_name = re.findall(find_name, request.url)[0]
        file_name = file_name.split('/')[-1]
        file_name = file_name[0:len(file_name) - 1]
        print(file_name, '正在下载！！！')
        return file_name
