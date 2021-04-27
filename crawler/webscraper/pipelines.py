# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging

from itemadapter import ItemAdapter

from crawler.webscraper.helpers.similar import similar
from src.models.residences import Residences


class WebscraperPipeline:
    def process_item(self, item, spider):
        return item


class AdLocationsPipeline:
    def open_spider(self, spider):
        res_table = Residences()
        ad_locations = res_table.get_ad_locations()

        spider.ad_locations = ad_locations

    def process_item(self, item, spider):
        if 'zone' in item:
            zone = item['zone'].lower()
            for ad_loc in spider.ad_locations:
                if zone in ad_loc.get('name'):
                    item['ad_location_id'] = ad_loc['ad_location_id']
                    return item

            for ad_loc in spider.ad_locations:
                if similar(zone, ad_loc.get('name')) > 0.75:
                    item['ad_location_id'] = ad_loc['ad_location_id']
                    return item

            logging.warning('Could not get field \'ad_location_id\', value for \'zone\': {}'.format(zone))
            raise ValueError('ad_location_id')
        else:
            logging.warning('Missing mandatory field \'zone\'')
            raise ValueError('zone')

        return item
