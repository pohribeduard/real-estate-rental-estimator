# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ResidenceItem(scrapy.Item):
    url = scrapy.Field()
    balconies = scrapy.Field()
    balconies_closed = scrapy.Field()
    bathrooms = scrapy.Field()
    built_area = scrapy.Field()
    livable_area = scrapy.Field()
    comfort = scrapy.Field()
    floor = scrapy.Field()
    floors = scrapy.Field()
    layout = scrapy.Field()
    rooms = scrapy.Field()
    zone = scrapy.Field()
    building_year = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()

