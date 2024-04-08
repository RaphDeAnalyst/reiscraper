# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name_of_item = scrapy.Field()
    description = scrapy.Field()
    full_price = scrapy.Field()
    sale_price = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    number_of_reviews = scrapy.Field()
    rating = scrapy.Field()
    type_color_available = scrapy.Field()
    
