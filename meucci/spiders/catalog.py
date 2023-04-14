import re

import scrapy
from scrapy.http import HtmlResponse


class Spider(scrapy.Spider):
    name = 'catalog'
    handle_httpstatus_list = (200,)

    def start_requests(self):
        yield scrapy.Request(
            'https://shop.meucci.ru/catalog/', callback=self.parse_categories
        )

    def parse_categories(self, response: HtmlResponse):
        sections = response.css('.main-section-list__item h2')
        for section in sections:
            section_name = section.css('a::text').get('').strip()
            if section_name in ('Новинки', 'Спецпредложения', 'Подарочные карты'):
                continue
            category_urls = section.xpath('./following-sibling::div/a/@href').getall()
            for category_url in category_urls:
                yield response.follow(
                    category_url + '?showby=100', callback=self.parse_product_listing
                )

    def parse_product_listing(self, response: HtmlResponse):
        # Pagination
        current_page = response.css('.pagination .active a::text').get()
        if current_page == '1':
            last_page = int(response.css('.pagination li a::text').getall()[-1])
            self.crawler.stats.inc_value(f'xxx/last-page/{last_page}')
            for page in range(2, last_page + 1):
                yield scrapy.Request(
                    response.url + f'&PAGEN_2={page}',
                    callback=self.parse_product_listing,
                )

        # Item URLs
        product_urls = response.css('div[data-entity="item"] > a::attr(href)').getall()
        for product_url in product_urls:
            yield response.follow(product_url, callback=self.parse_product)

        # Stats
        self.crawler.stats.inc_value('xxx/products', len(product_urls))

    def parse_product(self, response: HtmlResponse):
        yield {
            'path': '>'.join(
                response.css('.breadcrumb span[property="name"]::text').getall()[2:]
            ),
            'url': response.url,
            'name': response.css('.container h1::text').get(),
            'description': self._extract_product_description(response),
            'sku': response.css('.detail-info span[itemprop="mpn"]::text').get(),
            'price': (
                response.css('.detail-info meta[itemprop="price"]::attr(content)').get()
            ),
            'old_price': re.sub(
                r'[^\d]+', '', response.css('.detail-info .old-price::text').get('')
            ),
            'discount': (
                response.css('.detail-info .discount .value::text').re_first(r'\d+')
            ),
            'image': response.urljoin(
                response.css('.slide source::attr(srcset)').get()
            ),
            'attributes': self._extract_product_attributes(response),
            'promos': response.css('.detail-info .badge-sale::text').get(),
        }

    @staticmethod
    def _extract_product_description(response: HtmlResponse) -> str | None:
        q = '//a[@role="tab" and contains(., "Описание")]/@aria-controls'
        if description_tab_id := response.xpath(q).get():
            return (
                response.xpath(f'string(//div[@id="{description_tab_id}"])')
                .get()
                .strip()
            )
        return None

    @staticmethod
    def _extract_product_attributes(response: HtmlResponse) -> str:
        attributes = {}

        for attribute in response.css('.detail-info .props .prop'):
            name = attribute.css('.title::text').get('').strip().rstrip(':')
            if name == 'Перейти в категорию':
                continue
            value = attribute.css('.value::text').get('').strip()
            attributes[name] = value

        return '\n'.join(': '.join([name, value]) for name, value in attributes.items())
