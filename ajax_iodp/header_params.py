# 此请求头信息为通用,其中referer需要传入两个参数
Headers = {
    # Referer是变量
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Host': 'web.iodp.tamu.edu',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.68',
    'X-Requested-With': 'XMLHttpRequest'
}

# id一次传入20个，响应的数据是json
data_url = 'http://web.iodp.tamu.edu/limsM/DisplayGet-LORE?name={0}&username=guest&password=WsH/YEUqqrWDxD15zxsUPg==&id={1}&postretrieve=%7B%7D'
# 单独处理前三个report的url模板，该url直接指向对应的数据
data_url_3 = 'http://web.iodp.tamu.edu/limsM/SummaryReportGet-LORE?report={0}&username=guest&password=WsH%2FYEUqqrWDxD15zxsUPg%3D%3D&filters=%5B%22x_expedition%20in%20(%27{1}%27)%22%5D&postretrieve=%7B%22scale_id%22%3A%2211331%22%7D'
# 获取对应表头信息的url模板
header_url = 'http://web.iodp.tamu.edu/reference/HeaderDisplayGet-LORE?name={0}&scaleid=11331&splice=test'
data_url_params = {
    # name和id是变量
    'name': '',
    'id': [],
}
# 获取data_url需要的id序列，响应的是json
id_list_url = 'http://web.iodp.tamu.edu/limsM/AWorkingSetGet-LORE?username=guest&password=WsH%2FYEUqqrWDxD15zxsUPg%3D%3D&report={0}&postretrieve=%7B%7D&filters={1}'

id_list_url_params = {
    # filters传入Exception号即可（船号）
    'report': '',
    'filters': '%5B%22x_expedition%20in%20(%27{0}%27)%22%5D'
}
