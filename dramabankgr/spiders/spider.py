import scrapy

from scrapy.loader import ItemLoader

from ..items import DramabankgrItem
from itemloaders.processors import TakeFirst


class DramabankgrSpider(scrapy.Spider):
	name = 'dramabankgr'
	start_urls = ['https://dramabank.gr/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="cmsmasters_open_link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h2/text()').get()
		description = response.xpath('//div[@class="cmsmasters_text"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//abbr[@class="published"]/text()').get()

		item = ItemLoader(item=DramabankgrItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
