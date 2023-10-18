import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikiSpider.items import Article


def parse_item(response):
    item = Article()
    title = response.css('h1::text').get()
    print("Title is: " + title)
    item['title'] = title
    return item


class ArticleSpider(CrawlSpider):
    name = "article2"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["http://en.wikipedia.org/wiki/Python_(programming_language)"]

    rules = (
        Rule(
            LinkExtractor(allow=r'(/wiki/)((?!:).)*$'),
            callback="parse_item",
            follow=True
        ),
    )
