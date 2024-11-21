from pathlib import Path

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from datetime import datetime

class ShopSpider(scrapy.Spider):
    name = "ShopSpider"
    visited = set()

    allowed_substring = []
    restricted_substring = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)

        folder_name = Path(kwargs['output_path']) / kwargs["start_url"].strip("/").split("/")[-1]

        output_path = Path(folder_name)
        output_path.mkdir(exist_ok=True)

        feed_filename = output_path / f'%(batch_time)s.jsonl'


        spider.settings.set("FEED_FORMAT", "jsonlines", priority="spider")
        spider.settings.set("FEED_URI", str(feed_filename), priority="spider")

        return spider

    def __init__(self, start_url, product_pattern, restricted_pattern=None,*args, **kwargs):

        allowed_domain = start_url.strip("/").split("/")[-1]

        self.filename = allowed_domain
        self.start_urls = [start_url]

        self.allowed_substring = product_pattern.split(',')
        if restricted_pattern:
            self.restricted_substring = restricted_pattern.split(',')
        self.link_extractor = scrapy.linkextractors.lxmlhtml.LxmlLinkExtractor(allow_domains=[allowed_domain], unique=True)


    def parse(self, response):
        links = self.link_extractor.extract_links(response)
        for link in links:
            if link.url not in self.visited:
                self.visited.add(link.url)

                valid_url = False

                for substring in self.allowed_substring:
                    if substring in link.url:
                        valid_url = True
                        break

                for substring in self.restricted_substring:
                    if substring in link.url:
                        valid_url = False
                        break

                if valid_url:
                    yield {"url": link.url}

            yield scrapy.Request(url=link.url, callback=self.parse)
