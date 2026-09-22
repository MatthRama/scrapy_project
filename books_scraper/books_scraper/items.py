# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
import scrapy


@dataclass
class BooksScraperItem:
    # define the fields for your item here like:
    # name: str | None = None
    pass

class BookItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    star_rating = scrapy.Field()
    in_stock = scrapy.Field()
    thumbnail_url = scrapy.Field()
    detail_url = scrapy.Field()
    upc = scrapy.Field()
    description = scrapy.Field()
    number_available = scrapy.Field()
    category = scrapy.Field()
    image_url = scrapy.Field()

    image_urls = scrapy.Field()
    images = scrapy.Field()