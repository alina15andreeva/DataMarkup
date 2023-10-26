import scrapy
from scrapy.http import HtmlResponse
from sys import path

path.append('/Users/alinaandreeva/Downloads/practice5')
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://hh.ru/search/vacancy?from=suggest_post&hhtmFrom=main&search_field=name&search_field=company_name&search_field=description&text=Python&enable_snippets=false&L_save_area=true"]

    def parse(self, response:HtmlResponse):

        next_page = response.xpath("//a[@ata-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='serp-item__title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response:HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
