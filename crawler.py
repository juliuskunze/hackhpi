import scrapy

URL_REGEX = r"window\.open\('([^']+)"

class CVSpider(scrapy.Spider):
    name = 'cv_spider'
    start_urls = ['http://www.indeed.com/resumes?q=developer']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paging_offset = 0

    def parse(self, response):
        for url in response.css('.clickable_resume_card::attr(onclick)').re(URL_REGEX):
            yield scrapy.Request(response.urljoin(url), self.parse_resumes)
        self.paging_offset += 50
        if self.paging_offset > 10000:
            return
        yield scrapy.Request(self.start_urls[0] + '&start=' + str(self.paging_offset), self.parse)

    def parse_resumes(self, response):
        for resume_text in response.css('#resume').extract():
            yield {'resume': resume_text}

