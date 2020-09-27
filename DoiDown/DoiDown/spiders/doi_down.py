import pymysql
import scrapy
from scrapy import Request
import re
from ..items import DoidownItem


class DoiDownSpider(scrapy.Spider):
    name = 'doi_down'
    # allowed_domains = ['sci-hub.ren']
    connect = None
    cursor = None

    # start_urls = ['http://sci-hub.ren/']

    def start_requests(self):
        self.connect = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="xxxxxx",
            db="web_of_science")
        self.cursor = self.connect.cursor()
        self.cursor.execute("select doi from wos_document;")

        doi_lists = list(self.cursor.fetchall())

        for doi in doi_lists:
            if doi[0] is None:
                print('该DOI为空...')
            else:
                detail_url = 'https://www.sci-hub.ren/' + doi[0]
                print(detail_url)
                yield Request(detail_url, callback=self.parse)

        self.connect.close()

    def parse(self, response):
        print('解析中!!!')
        detail_url_list = response.xpath('//*[@id="buttons"]/ul/li[2]/a/@onclick')
        item = DoidownItem()
        item['file_urls'] = []
        if len(detail_url_list) == 0:
            print('*' * 10 + '已自动跳转第三方网站，不予处理!!!' + '*' * 10)
        else:
            # 提取第一个目标Selector的内容
            target = detail_url_list.extract_first()
            find_url = re.compile(r"href='(.*?)'")
            target_url = re.findall(find_url, target)[0]
            if target_url[0] != 'h':
                target_url = 'https:' + target_url
            item['file_urls'].append(target_url)
            yield item
