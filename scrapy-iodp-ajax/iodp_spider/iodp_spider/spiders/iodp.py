import scrapy
from .tool import *
import os
from ..pipelines import save_header
from scrapy import Request
from ..items import IodpSpiderItem


class IodpSpider(scrapy.Spider):
    name = 'iodp'
    allowed_domains = ['web.iodp.tamu.edu']

    '''
    1、拿到report信息，有34个
    2、拿到Exception信息，即船号列表
    3、由id_list_url携带report+船号，获取id列表
    4、由data_url携带report+id序列（每次最多20个），获取数据
    5、每一个url携带的参数都必须经过url加密，也就是将url中携带的参数加密后，拼接成目标url
    '''

    def start_requests(self):
        if not os.path.exists('./CSV/'):
            os.mkdir('./CSV/')

        exception_list = get_json(
            url='http://web.iodp.tamu.edu/limsR/DrillDownDetailGet-OVERVIEW?context=expedition&filter=%5B%22to_number(regexp_substr(expedition%2C%20%27%5B0-9%5D%2B%27))%20between%20313%20and%20348%22%5D&order=desc')
        print(exception_list)
        # report_list = [ 'samples',  'corephoto', 'lsimg', 'wrlscjpg', 'closeup', 'tsimage', 'microimg', 'gra', 'ms', 'mspoint', 'mad', 'ngr', 'pwl', 'pwc', 'pwb', 'rsc', 'avs', 'tor', 'penetrate', 'dhtemp', 'tcon', 'srmsection', 'srmdiscrete', 'iw_internal', 'icpaes_internal', 'carbonates_internal', 'sranl', 'gaselements_internal', 'xrd']
        report_list = ['sem']
        for report in report_list:
            # 前三个report的数据ajax加载方式不同，已经单独处理
            for exception in exception_list:
                date_id_list = list(get_data_id(report, exception))
                save_header(report, exception)
                for i in range(0, len(date_id_list), 20):
                    id = date_id_list[i:i + 20:1]
                    id_encode = data_url_encrypt(id)
                    # 传入report+加密后的id字符串，得到指向目标数据的url
                    url = data_url.format(report, id_encode)
                    item = IodpSpiderItem()
                    item['report'] = report
                    item['exception'] = exception
                    yield Request(url=url, callback=self.parse, meta={'item': item})

    def parse(self, response):
        # 获取url对应的data，并交付给pipline保存
        item = response.meta['item']
        print(item['report'],item['exception']+'获取响应成功')
        item['data_text'] = response.json()
        yield item
