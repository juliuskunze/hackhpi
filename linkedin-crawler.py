import logging
import re

import scrapy

from html_parsing import strip_tags
from proxies import read_proxies

PERSON_REGEX = re.compile(r"(https://www\.linkedin\.com/in/[^\"]+)")
MEMBER_ID_REGEX = re.compile(r"^https://www\.linkedin\.com/in/([^?]+)")

proxies = read_proxies()

class CVSpider(scrapy.Spider):
    name = 'cv_spider'
    start_urls = ['https://www.linkedin.com/in/jonas-pohlmann-77a64b82']
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 543
    }
    http_proxy = proxies[0]
    handle_httpstatus_list = [999]


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.crawled = set()
        self.proxy_iterator = iter(proxies)
        next(self.proxy_iterator)

    def request_for_url(self, url):
        return scrapy.Request(url, self.parse)

    def parse(self, response):
        if response.status == 999:
            self.http_proxy = next(self.proxy_iterator)
            yield self.request_for_url(response.url)
            return

        member = MEMBER_ID_REGEX.match(response.url).group(1)
        if member not in self.crawled:
            self.crawled.add(member)
            for display in response.css('li.position'):
                yield self.get_entry(display, member)

        for url in response.css('a::attr(href)').re(PERSON_REGEX):
            yield self.request_for_url(response.urljoin(url))

    def get_entry(self, display, member):
        return {
            'member': member,
            'title': strip_tags(display.css('header h4 a span').extract_first()),
            'company': strip_tags(display.css('header h5.item-subtitle a span').extract_first()),
            'dates': display.css('time::text').extract_first()
        }
