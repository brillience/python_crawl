import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import re
import os


class IodpSpider(scrapy.Spider):
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable_gpu')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.chrome = webdriver.Chrome(chrome_options=options)

    name = 'iodp'
    allowed_domains = ['web.iodp.tamu.edu']
    start_urls = ['http://web.iodp.tamu.edu/OVERVIEW/']

    def parse(self, response):
        tr_list = response.xpath('//*[@id="gridBox"]/tr')
        print('共{0}张表'.format(len(tr_list)))
        for tr in tr_list:
            td_list = tr.xpath('./td')
            for td in td_list[1:]:
                href = td.xpath('./a/@href').extract_first()
                if href != None and href[0] != 'h':
                    yield response.follow(url=href, callback=self.parse_detail)

    def parse_detail(self, response):
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
        headWrited = True
        if not os.path.exists('../CSV/'):
            os.mkdir('../CSV/')
        with open('../CSV/' + filename + '.csv', 'a', encoding="utf-8",newline='') as f:
            print('*'*10+'正在写入'+ filename + '.csv'+'*'*10)
            writer = csv.DictWriter(f, head)
            writer.writeheader()
            data = []
            data_tr_list = response.xpath('//*[@id="cm_rpt_body"]/tr | //*[@id="dm_rpt_body"]/tr')
            for tr in data_tr_list:
                data_td_list = tr.xpath('./td')
                data.clear()
                for td in data_td_list:
                    data.append(str(td.xpath('./text()').extract_first()))
                writer.writerow(dict(zip(head,data)))
        f.close()
        print('*' * 10 + '完成写入' + filename + '.csv' + '*' * 10)

    def __del__(self):
        self.chrome.quit()
