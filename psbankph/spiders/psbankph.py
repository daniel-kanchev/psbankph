import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from psbankph.items import Article


class psbankphSpider(scrapy.Spider):
    name = 'psbankph'
    start_urls = ['https://www.psbank.com.ph/whats-new/']

    def parse(self, response):
        articles = response.xpath('//div[@class="col-md-9"]/div')
        for article in articles:
            num = len(article.xpath('.//div[@class="wTitle"]'))
            print(num)
            for i in range(num):
                item = ItemLoader(Article())
                item.default_output_processor = TakeFirst()

                title = article.xpath(f'.//div[@class="wTitle"][{i+1}]/text()').get()
                if title:
                    title = title.strip()

                date = article.xpath('./@id').get()
                if date:
                    date = " ".join(date.split())
                if 'Latest' in date:
                    continue

                content = article.xpath(f'.//div[@class="wRitchtext"][{i+1}]//text()').getall()
                content = [text.strip() for text in content if text.strip() and '{' not in text]
                content = " ".join(content).strip()

                item.add_value('title', title)
                item.add_value('date', date)
                item.add_value('content', content)

                yield item.load_item()



