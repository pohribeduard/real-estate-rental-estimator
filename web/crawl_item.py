from scrapy.crawler import CrawlerProcess, CrawlerRunner
import re
from twisted.internet import reactor
from crawler.webscraper.helpers.similar import similar
from crawler.webscraper.pipelines import AdLocationsPipeline
from crawler.webscraper.spiders.imobiliare import Imobiliare
from src.models.residences import Residences


def crawl_item(url_to_crawl):
    items = []

    # pipeline to fill the items list
    class ItemCollectorPipeline(object):
        def __init__(self):
            self.ids_seen = set()

        def process_item(self, item, spider):
            items.append(item)

    class FindZonePipeline(object):
        def process_item(self, item, spider):
            res_table = Residences()
            zones = res_table.get_zones()

            if 'zone' in item:
                zone_from_item = item['zone'].lower()
                for zone in zones:
                    if zone_from_item in zone.get('name').lower():
                        item['zone_id'] = zone['zone_id']
                        return item

                for zone in zones:
                    if similar(zone_from_item, zone.get('name').lower()) > 0.75:
                        item['zone_id'] = zone['zone_id']
                        return item

            return item

    # create a crawler process with the specified settings
    # process = CrawlerProcess({
    #     'USER_AGENT': 'scrapy',
    #     'LOG_LEVEL': 'INFO',
    #     'ITEM_PIPELINES': {ItemCollectorPipeline: 302,
    #                        FindZonePipeline: 301, }
    # })

    # start the spider
    # process.crawl(Imobiliare,
    #               url_to_crawl=url_to_crawl)
    # process.start()

    runner = CrawlerRunner({
        'USER_AGENT': 'scrapy',
        'LOG_LEVEL': 'INFO',
        'ITEM_PIPELINES': {ItemCollectorPipeline: 302,
                           FindZonePipeline: 301, }
    })

    d = runner.crawl(Imobiliare, url_to_crawl=url_to_crawl)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


    # print the items
    for item in items:
        print("url: " + item['url'])

        res_dict = {
            'balconies': item.get('balconies') if 'balconies' in item else None,
            'balconies_closed': item.get('balconies_closed') if 'balconies_closed' in item else None,
            'bathrooms': item.get('bathrooms') if 'bathrooms' in item else None,
            'built_area': item.get('built_area') if 'built_area' in item else None,
            'livable_area': item.get('livable_area') if 'livable_area' in item else None,
            'comfort': item.get('comfort') if 'comfort' in item else None,
            'floor': item.get('floor') if 'floor' in item else None,
            'floors': item.get('floors') if 'floors' in item else None,
            'furnished': item.get('furnished') if 'furnished' in item else None,
            'layout': item.get('layout') if 'layout' in item else None,
            'price': item.get('price') if 'price' in item else None,
            'rooms': item.get('rooms') if 'rooms' in item else None,
            'zone_id': item.get('zone_id') if 'zone_id' in item else None,
            'building_year': item.get('building_year') if 'building_year' in item else None
        }

        print()

        res_dict = {key: val for key, val in res_dict.items() if val is not None}

        print()
        new_dict = {}
        for key, val in res_dict.items():
                new_val = re.sub(r'[^0-9,\.]', '', str(val))
                if new_val:
                    new_dict[key] = float(new_val.replace(',','.'))

        return new_dict