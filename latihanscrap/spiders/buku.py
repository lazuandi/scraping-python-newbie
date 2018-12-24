# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class BukuSpider(scrapy.Spider):
    name = 'buku'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        books_url = response.xpath('//h3/a/@href').extract()
        for book in books_url:
            book_url = response.urljoin(book)
            yield Request(book_url, callback=self.parse_book)

        next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        next_url = response.urljoin(next_page)
        yield Request(next_url, callback=self.parse)

    def parse_book(self, response):
        image = response.xpath('//div[@class="item active"]/img/@src').extract_first()
        title = response.xpath('//div[@class="col-sm-6 product_main"]/h1/text()').extract_first()
        price = response.xpath('//div[@class="col-sm-6 product_main"]/p/text()').extract_first()
        yield{
            "image":image,
            "title":title,
            "price":price
        }