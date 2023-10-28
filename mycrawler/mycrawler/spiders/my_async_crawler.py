import asyncio
import aiohttp
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mycrawler.items import MyCrawlerItem
import time


class MyAsyncCrawlerSpider(CrawlSpider):
    def __init__(self, *args, **kwargs):
        super(MyAsyncCrawlerSpider, self).__init__(*args, **kwargs)
        self.visited_urls = set()
        self.items_processed = 0
        self.start_time = time.time()

        with open('domains.txt', 'r') as domains_file:
            self.allowed_domains = [line.strip() for line in domains_file]

        with open('start_urls.txt', 'r') as start_urls_file:
            self.start_urls = [line.strip() for line in start_urls_file]

    name = 'my_async_crawler'
    rules = (
        Rule(LinkExtractor(allow=('/')), callback='parse_start_page', follow=True),
    )

    async def parse_start_page(self, response):
        item = MyCrawlerItem()
        item['url'] = response.url
        if response.url not in self.visited_urls:
            self.visited_urls.add(response.url)
            yield item
            self.items_processed += 1


async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def run_crawler_and_measure_speed():
    crawler = MyAsyncCrawlerSpider()
    for url in crawler.start_urls:
        html = await fetch_url(url)
        response = scrapy.http.HtmlResponse(url=url, body=html.encode('utf-8'))
        await crawler.parse_start_page(response)

    end_time = time.time()
    elapsed_time = end_time - crawler.start_time
    crawl_speed = crawler.items_processed / elapsed_time
    print(f'Crawling speed: {crawl_speed:.2f} items/second')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_crawler_and_measure_speed())
