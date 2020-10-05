from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import re
import os
from scrapy import Request
import time
from scrapy.http import HtmlResponse

class IodpSpider(RedisSpider):
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable_gpu')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.chrome = webdriver.Chrome(chrome_options=options)

    name = 'iodp'
    allowed_domains = ['web.iodp.tamu.edu']
    # start_urls = ['http://web.iodp.tamu.edu/OVERVIEW/']
    redis_key = 'iodp'

    def make_requests_from_url(self, url):
        return Request(url,dont_filter=True,meta={'get':True},callback=self.parse)

    def parse(self, response):
        tr_list = response.xpath('//*[@id="gridBox"]/tr')
        print('共{0}张表'.format(len(tr_list)))
        for tr in tr_list:
            td_list = tr.xpath('./td')
            for td in td_list[1:]:
                href = td.xpath('./a/@href').extract_first()
                if href != None and href[0] != 'h':
                    yield response.follow(url=href, callback=self.parse_detail, meta={'get': True})
    def save_data(self, response):
        head = []
        head_td_list = response.xpath('//*[@id="dm_rpt_head"]/tr[1]/td | //*[@id="cm_rpt_body"]/tr[1]/td')
        print(response.url)
        if len(head_td_list):
            for td in head_td_list:
                head.append(str(td.xpath('./text()').extract_first()))

        # 完成表头提取，开始创建文件并提取每行的数据，并写入文件
        # http://web.iodp.tamu.edu/LORE/?appl=LORE&reportName=holesum&action=show&filters=%5B%22x_expedition%20in%20(%27385%27)%22%5D
        find_filename = re.compile(r"LORE&reportName=(.*?)&action=")
        filename = re.findall(find_filename, response.url)[0]
        # headWrited = True
        if not os.path.exists('./CSV/'):
            os.mkdir('./CSV/')
        with open('./CSV/' + filename + '.csv', 'a', encoding="utf-8", newline='') as f:
            print('*' * 10 + '正在写入' + filename + '.csv' + '*' * 10)
            writer = csv.DictWriter(f, head)
            writer.writeheader()
            data = []
            data_tr_list = response.xpath('//*[@id="cm_rpt_body"]/tr | //*[@id="dm_rpt_body"]/tr')
            for tr in data_tr_list:
                data_td_list = tr.xpath('./td')
                data.clear()
                for td in data_td_list:
                    data.append(str(td.xpath('./text()').extract_first()))
                writer.writerow(dict(zip(head, data)))
        f.close()
        print('*' * 10 + '完成写入' + filename + '.csv' + '*' * 10)

    def parse_detail(self, response):
        self.save_data(response)
        self.nextPage(response)

    def nextPage(self, response):
        # 判断是否需要翻页，如需翻页则还需爬取翻页后的数据
        # 先判断是否需要翻页；不需要，跳过；需要：点击翻页，等待渲染，保存数据，递归处理
        if len(response.xpath('//*[@id="dm_feedback_last"]')) != 0:
            text = str(response.xpath('//*[@id="dm_feedback_last"]').extract_first())
            print(text)
            # <span id="dm_feedback_last" style="margin-left:5px;">200 rows displayed for 200 tests of 304</span>
            find = re.compile(r">(.*?)</span>")
            text = re.findall(find, text)[0]
            print(text)
            s = text.split()
            sub = int(s[-4])
            tol = int(s[-1])
            print('当前url的页面情况', '子页面:', sub, '总页面：', tol)
            if (tol - sub) <= 5:
                pass
            else:
                button = self.chrome.find_element_by_xpath('//*[@id="dm_next"]')
                button.click()
                time.sleep(30)
                page = self.chrome.page_source
                cresponse = HtmlResponse(url=response.url, body=page, encoding='utf-8')
                self.save_data(cresponse)
                self.nextPage(cresponse)

    def __del__(self):
        self.chrome.quit()
