import requests
from .header_params import *
from urllib.parse import quote_plus

'''
1、拿到report信息，有34个
2、拿到Exception信息，即船号列表
3、由id_list_url携带report+船号，获取id列表
4、由data_url携带report+id序列（每次最多20个），获取数据
5、每一个url携带的参数都必须经过url加密，也就是将url中携带的参数加密后，拼接成目标url
'''

param = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.68'
}


def get_json(url, params=param):
    """
    发送url请求获取json数据
    :param params: 请求头部信息
    :param url:
    :return:list，元素为str
    """
    return requests.get(url=url, params=params).json()


def get_report():
    print('正在获取report...')
    report = []
    report_id_list = get_json(
        url='http://web.iodp.tamu.edu/limsR/ReportListGet-OVERVIEW?filter=%5B%22to_number(regexp_substr(expedition%2C%20%27%5B0-9%5D%2B%27))%20between%20313%20and%20348%22%5D')
    url_template_report = 'http://web.iodp.tamu.edu/limsR/GridGet-OVERVIEW?context=expedition&filter=%5B%22to_number(regexp_substr(expedition%2C%20%27%5B0-9%5D%2B%27))%20between%20313%20and%20348%22%5D&report_id={}&order=desc'
    for id in report_id_list:
        url = url_template_report.format(id)
        report_name = dict(get_json(url)[0])['href'].split('=')[-1]
        report.append(report_name)
    print('获取report完毕：')
    print(len(report),'个report')
    print(report)
    return report


def get_data_id(report, exception):
    """
    返回对应report的数据的id列表
    :param report: 主题
    :param exception: 船号
    :return: list
    """
    print('正在获取当前' + report + ' ' + exception + '数据的id')
    filters = id_list_url_params['filters']
    filters = filters.format(exception)
    url = id_list_url.format(report, filters)
    print(url)
    print('完毕！！！')
    return get_json(url, Headers)


def data_url_encrypt(id_list):
    """
    对获取数据url进行url加密，因为加密后才可以请求获取到数据
    :param id_list: 对应数据的id，每次最多20个
    :return: url , str
    """
    id_list = str(id_list)
    return quote_plus(id_list).replace('+', '')



