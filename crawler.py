import scrapy

URL_REGEX = r"window\.open\('([^']+)"

proxies = [
    '146.52.84.73:8080',
    '27.122.12.45:3128',
    '104.215.255.64:80',
    '77.123.18.56:81',
    '113.108.82.29:80',
    '174.36.234.214:8888',
    '119.29.233.113:80',
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
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
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
        return scrapy.Request(url, self.parse_resumes, errback=lambda x: self.error_resume(x, url))

    def parse(self, response):
        for url in response.css('.clickable_resume_card::attr(onclick)').re(URL_REGEX):
            yield self.request_for_url(response.urljoin(url))
        self.paging_offset += 50
        if self.paging_offset > 10000:
            return
        yield scrapy.Request(self.start_urls[0] + '&start=' + str(self.paging_offset), self.parse)

    def parse_resumes(self, response):
        for resume_text in response.css('#resume').extract():
            yield {'resume': resume_text}

    def error_resume(self, error, url):
        self.http_proxy = next(self.proxy_iterator)
        yield self.request_for_url(url)
