import logging
import re

import scrapy

from proxies import read_proxies

URL_REGEX = r"window\.open\('([^']+)"

proxies = read_proxies()

class CVSpider(scrapy.Spider):
    name = 'cv_spider'
    start_urls = ['http://www.indeed.com/resumes?q=developer']
    download_delay = 1
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 543
    }
    http_proxy = proxies[0]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paging_offset = 400
        self.proxy_iterator = iter(proxies)
        next(self.proxy_iterator)

    def request_for_url(self, url):
        return scrapy.Request(url, self.parse_resumes)

    def parse(self, response):
        for url in response.css('.clickable_resume_card::attr(onclick)').re(URL_REGEX):
            yield self.request_for_url(response.urljoin(url))
        self.paging_offset += 50
        self.http_proxy = next(self.proxy_iterator)
        yield scrapy.Request(self.start_urls[0] + '&start=' + str(self.paging_offset), self.parse)

    def get_entry(self, display):
        return {
            'title': display.css('.work_title').extract(),
            'company': display.css('.work_company').extract(),
            'dates': display.css('.work_dates').extract()
        }

    def parse_resumes(self, response):
        for resume in response.css('#resume'):
            logging.info('Got resume')
            displays = resume.css('.data_display')
            entries = [self.get_entry(display) for display in displays]

            result = {
                'resume': resume.extract(),
                'entries': entries
            }
            yield result
