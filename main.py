import scrapy
from scrapy.crawler import CrawlerProcess
import time


class LomparsSpider(scrapy.Spider):
    name = 'lompars'
    allowed_domains = ['победа-63.рф']
    start_urls = ['https://www.sofascore.com/']

    def start_requests(self):
        start_point = 'https://победа-63.рф/catalog/kompyuternaya-tehnika/noutbuki/1/?q=60'
        last_page = 51

        urls = [
            'https://www.sofascore.com/football/',
            'https://www.sofascore.com/basketball/',
            'https://www.sofascore.com/tennis/',
            'https://www.sofascore.com/table-tennis/',
            'https://www.sofascore.com/ice-hockey/',
            'https://www.sofascore.com/esports/',
            'https://www.sofascore.com/handball/',
            'https://www.sofascore.com/volleyball/',
            'https://www.sofascore.com/baseball/',
            'https://www.sofascore.com/american-football/',
            'https://www.sofascore.com/motorsport/',
            'https://www.sofascore.com/cricket/',
            'https://www.sofascore.com/rugby/',
            'https://www.sofascore.com/darts/',
            'https://www.sofascore.com/snooker/',
            'https://www.sofascore.com/futsal/',
            'https://www.sofascore.com/badminton/',
            'https://www.sofascore.com/aussie-rules/',
            'https://www.sofascore.com/beach-volley/',
            'https://www.sofascore.com/waterpolo/',
            'https://www.sofascore.com/bandy/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        items = response.xpath('//div[@class="card-content"]')
        for element in items:
            yield {
                'discipline': element.xpath('.//meta[@itemprop="name"]/@content')[0].get(),
                'title': element.xpath('.//meta[@itemprop="name"]/@content')[0].get(),
                'price': element.xpath('.//div[@class="card-price"]/@content')[0].get(),
                'link': element.xpath('.//a[@class="card-title"]/@href')[0].get()
            }


process = CrawlerProcess(settings={
    "FEEDS": {
        "out.json": {"format": "json"},
    },
})
process.crawl(LomparsSpider)
process.start()
