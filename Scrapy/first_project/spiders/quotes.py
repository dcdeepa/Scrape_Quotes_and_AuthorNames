import scrapy
from ..items import FirstProjectItem
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/login/',
    ]

    def parse(self, response):
        token=response.css('form input::attr(value)').get()
	return FormRequest.form_response(response, formdata={
            'csrf_token'=token ,
            'username'='deepa' ,
            'password' ='deepa'
          } , callback = self.start_scraping )
	
    def start_scraping(self,response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
