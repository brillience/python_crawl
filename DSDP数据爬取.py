# coding=utf-8
import re
from bs4 import BeautifulSoup
import urllib.request as urlreq
import urllib.error as urlerr
import csv
import os
import requests
def main():
    baseurl = "https://mlp.ldeo.columbia.edu/logdb/scientific_ocean_drilling/result/"
    html = askurl(baseurl)
    data = getdate(html)
    save(data)
    download(data)
def download(data):
    # 第一步：提取出data列表内的所有二级网页的链接
    # 第二步：在二级网页中提取所有压缩包的下载地址，注意这里采用二维列表，将属于同一个二级网页的压缩包的下载地址放在同一个子列表中
    # 第三步：将在同一个子列表的压缩包存储在一个文件夹中，并将文件夹命名为相应的名字
    urls = []
    # 这是二级网页url
    folder_name = []
    find_folder_name = re.compile(r'(.*?) link')
    find_url = re.compile(r'link:(.*?) ')
    for item in data[2:len(data)-4]:
        # 最后四个二级网页的链接需要用户名和密码进行身份验证，所以暂时舍弃
        folder_name.append(re.findall(find_folder_name, item[3])[0])
        urls.append(re.findall(find_url, item[3])[0])
    # 开始提取每个二级网页中的压缩包下载链接
    download_urls = []
    # 这里一个二维的列表，最内层存的是文件的下载链接
    for item in urls:
        # 开始解析二级网页提取下载链接
        html = askurl(item)
        find_down_url = re.compile(r'<A href=(.*?) > Download</A>')
        temp_down_urls = re.findall(find_down_url, str(html))
        print(temp_down_urls)
        download_urls.append(temp_down_urls)
    # 开始创建相应名字的文件夹，并将文件下载
    for i in range(0, len(folder_name)):
        path = '.\\download_files\\'+folder_name[i]
        if not os.path.exists(path):
            os.mkdir(path)
        # 接下来，第一步提取带下载文件的文件名，第二步下载文件到指定文件夹
        zip_name = []
        for j in download_urls[i]:
            zip_name.append(j.split('/')[-1])
        print(zip_name)
        for count in range(0, len(zip_name)):
            with open(path+'\\'+zip_name[count], 'wb+') as f:
                # 在这里设置超时机制,超时就五次重连
                times = 0
                while 1:
                    try:
                        down = requests.get(urls[i] + download_urls[i][count], timeout=10)
                        print(zip_name[count]+'正在下载......')
                        f.write(down.content)
                        print(zip_name[count] + '下载完毕！！！')
                        break
                    except requests.exceptions.RequestException as e:
                        times += 1
                        print('正在重试！！！')
                        if times >= 5:
                            # 超时重连5次失败时
                            print(str(e))
                            print(zip_name[count] + '下载失败！！！')
                            break

            f.close()
def askurl(url):
    # 向服务器发送请求
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    }

    request = urlreq.Request(url, headers=head)
    html = ""
    try:
        response = urlreq.urlopen(request)
        html = response.read().decode("utf-8")
        print("获取服务器响应成功！！！")
    except urlerr.URLError as e:
        print("出现异常-->" + str(e))
    return html
def getdate(html):
    soup = BeautifulSoup(html, "html.parser")
    print("解析网页ing...")
    # print(soup.find_all('tr'))
    find_td = re.compile(r'<td>(.*?)</td>')
    items = soup.find_all('tr')
    data = []
    for item in items[1:len(items)-1]:
        item = str(item)
        sub_data = re.findall(find_td, item)
        if len(sub_data) >= 4:
            temp_str = (' link:https://mlp.ldeo.columbia.edu/' + re.findall(r'href="(.*?)"', sub_data[3])[0][1:] + ' ')
            sub_data[3] = re.findall(r'>(.*?)</a>', str(sub_data[3]))[0]
            sub_data[3] += temp_str
        data.append(sub_data)
    return data
def save(data):
    headers = ['YEAR', 'PROGRAM', 'LEG/EXP', 'HOLE', 'LOCATION', 'OCEAN/SEA']
    with open("data_list.csv", "a+", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for i in data[2:]:
            writer.writerow(i)
        f.close()
    print("数据列表爬取完毕！！！")

if __name__ == "__main__":
    main()
