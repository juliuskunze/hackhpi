import logging

import scrapy

URL_REGEX = r"window\.open\('([^']+)"

proxies = [
    '203.223.143.51:8080',
    '203.223.143.51:8080',
    '46.101.147.13:80',
    '54.179.146.162:8083',
    '123.30.191.141:80',
    '200.233.154.5:80',
    '220.130.196.155:8080',
    '85.204.229.47:81'
]

class CVSpider(scrapy.Spider):
    name = 'cv_spider'
    start_urls = ['http://www.indeed.com/resumes?q=developer']
    download_delay = 1
    user_agent = 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; XH; rv:8.578.498) fr, Gecko/20121021 Camino/8.723+ (Firefox compatible)'
    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 543
    }
    http_proxy = proxies[0]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paging_offset = 0
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
