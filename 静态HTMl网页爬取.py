# coding=utf-8
import re
from bs4 import BeautifulSoup
import urllib.request as urlreq
import urllib.error as urlerr
import csv
def main():
    baseurl = "https://mlp.ldeo.columbia.edu/logdb/scientific_ocean_drilling/result/"
    html = askurl(baseurl)
    data = getdate(html)
    save(data)

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
        if len(sub_data) >= 4 :
            sub_data[3] = re.findall(r'>(.*?)</a>', str(sub_data[3]))[0]
        #有一个 <a target=_blank href="/data/dsdp/leg8/70A/">70A</a> 的内容 需要单独处理，对应位置sub_data[3]
        data.append(sub_data)
    return data
def save(data):
    headers = ['YEAR', 'PROGRAM', 'LEG/EXP', 'HOLE', 'LOCATION', 'OCEAN/SEA']
    with open("data.csv", "a+", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for i in data[2:]:
            writer.writerow(i)
        f.close()
    print("数据爬取完毕！！！")

if __name__ == "__main__":
    main()
