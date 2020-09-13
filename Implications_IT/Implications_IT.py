#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/9/13 9:07
# @Author : ZhangXiaobo
# @Software: PyCharm
import os
import time
from multiprocessing import Pool

import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
}

baseurl = 'https://homepages.uc.edu/~thomam/Implications_IT/pdf/'


def get_urls(url):
    # 提取当前页面的所有文件或者二级网页地址
    page_source = requests.get(url, headers=headers).text
    tree = etree.HTML(page_source)
    tr_list = tree.xpath('//tr')
    sub_urls = []
    for tr in tr_list[3:-1]:
        sub_url = tr.xpath('./td[2]/a/@href')[0]
        sub_urls.append(url + sub_url)
    return sub_urls


def hand_dir(url):
    # 创建二级网页对应的文件夹，并返回文件夹名字
    dir_name = url.split('/')[-2]
    if not os.path.exists("./Implications_IT" + '/' + dir_name):
        os.mkdir("./Implications_IT" + '/' + dir_name)
        print('已创建', dir_name, '文件夹')
    return dir_name


def down_file(url, path):
    # 指定下载地址和保存路径
    data_name = url.split('/')[-1]
    print('正在下载', data_name, path)
    print(url)
    data = requests.get(url).content
    with open(path + '/' + data_name, 'wb') as f:
        f.write(data)
    f.close()
    print(data_name, '下载完毕!!!')
    time.sleep(10)


def main():
    base_path = "./Implications_IT"
    if not os.path.exists(base_path):
        os.mkdir(base_path)
        print('已创建', 'Implications_IT', '文件夹！！！')
    url1 = []
    # 当前可下载的文件
    url2 = []
    # 二级网页，一个新的文件夹下的文件处理
    for url in get_urls(baseurl):
        if url[-1] == 'f':
            url1.append(url)
        else:
            url2.append(url)

    print('开始处理当前页面的文件')
    # for url in url1:
    #     # 下载当前baseurl的文件
    #     down_file(url, base_path)
    pool = Pool(8)
    url_path1 = list(zip(url1, [base_path] * len(url1)))
    pool.starmap(down_file, url_path1)

    print('开始处理当前页面的二级页面')
    for url in url2:
        # 处理二级网页
        path = base_path + '/' + hand_dir(url)
        urls = get_urls(url)
        # 拿到了二级网页中的文件的下载地址
        # for l in urls:
        #     print(l)
        #     down_file(l, path)
        url_path2 = list(zip(urls, [path] * len(urls)))
        pool.starmap(down_file, url_path2)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
