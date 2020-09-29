# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import time


class IodpDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod


    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        spider.chrome.get(request.url)
        time.sleep(25)    # 等待完整加载ajax后的页面
        page_text = spider.chrome.page_source
        return HtmlResponse(url=request.url,body=page_text, encoding='utf-8', request=request)
