import requests
from lxml import etree
import re
import time
from db_operate import get_id_and_doi

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    }
def main():
    baseurl = "https://www.sci-hub.ren/"
    items = get_id_and_doi()
    for item in items:
        if items[item] is None:
            print(item,'无doi号...')
        else:
            down(file_name=item,url=baseurl+items[item])
            time.sleep(30)
def down(file_name,url):
    # url = "https://www.sci-hub.ren/10.1144/jm.19.2.139"
    page = requests.get(url,headers=headers).text
    tree = etree.HTML(page)
    onclick_list = tree.xpath('//*[@id="buttons"]/ul/li[2]/a/@onclick')
    if len(onclick_list)==0:
        print("已自动跳转到第三方网站，不予处理",file_name,"下载失败")
        return
    onclick = onclick_list[0]
    find_target_url = re.compile(r'location.href=(.*?)?download=true')
    target_url = re.findall(find_target_url,str(onclick))[0]
    target_url = target_url[1:len(target_url)-1]
    # 这里有的没有https
    if target_url[0]!='h':
        target_url = 'https:'+target_url
    print(target_url)
    times =0
    while 1:
        try:
            start_time = time.time()
            down = requests.get(target_url,headers=headers)
            print(file_name,"正在下载...")
            with open('./'+file_name+'.pdf','wb') as fp:
                fp.write(down.content)
            fp.close()
            print("下载完毕！！！"+ "    " + "耗时:",time.time()-start_time,"s")
            break
        except Exception as e:
            times+=1
            print("正在重试！！！")
            if times>=5:
                print(str(e))
                print(file_name,"下载失败！！！")
                break
if __name__ == "__main__":
    start_time = time.time()
    print("***"*10)
    main()
    print("***"*10)
    print('共耗时：',time.time()-start_time,'s')
