# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from DoiDown.DoiDown.settings import USER_AGENT_LIST, PROXY_http, PROXY_https
import random
from scrapy.http import HtmlResponse

class DoidownSpiderMiddleware:
    # 该函数拦截所有正常的请求
    def process_request(self, request, spider):
        # 随机选择一个UA
        user_agent = random.choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = user_agent

    # 该函数会拦截所有响应对象
    def process_response(self, request, response, spider):
        spider.chrome.get(request.url)
        spider.chrome.implicitly_wait(10) # 等待完整加载ajax后的页面
        page_text = spider.chrome.page_source
        return HtmlResponse(body=page_text,encoding='utf-8',request=request)

    # 异常处理，IP代理就在这里写
    def process_exception(self, request, exception, spider):
        # 设置代理ip
        if request.url.split(':')[0] == 'http':
            request.meta['proxy'] = 'http://' + random.choice(PROXY_http)
        else:
            request.meta['proxy'] = 'https://' + random.choice(PROXY_https)
