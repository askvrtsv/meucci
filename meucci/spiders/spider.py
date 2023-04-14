import scrapy
from scrapy.http import HtmlResponse


class Spider(scrapy.Spider):
    name = 'spider'
    handle_httpstatus_list = (200,)

    def start_requests(self):
        request = scrapy.Request(
            'http://quotes.toscrape.com',
            callback=self.parse_quotes,
        )
        yield request

    def parse_quotes(self, response: HtmlResponse):
        quotes = response.css('.quote')
        for quote in quotes:
            item = {
                'name': quote.css('.text::text').get(),
            }
            yield item

        next_page_url = response.css('.pager .next a::attr("href")').get()
        if next_page_url:
            request = response.follow(
                next_page_url,
                callback=self.parse_quotes,
            )
            yield request
