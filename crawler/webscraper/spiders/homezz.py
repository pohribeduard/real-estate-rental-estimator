import scrapy
from itemloaders.processors import MapCompose
from scrapy.http import Response

from crawler.webscraper.itemloaders import ResidenceItemLoader


class HomeZZ(scrapy.Spider):
    name = 'homezz.ro'
    allowed_domains = [
        'homezz.ro'
    ]

    start_urls = [
        'https://homezz.ro/anunturi_apartamente_de-inchiriat_in-bucuresti-if.html'
    ]

    layout_mapping = {
        'decomandat': 1,
        'semidecomandat': 2,
        'circular': 3,
        'nedecomandat': 4,
        'vagon': 5
    }

    def __init__(self, url_to_crawl=None, **kwargs):
        """
        Used in order to receive the url from the console
        :param filename:
        :param kwargs:
        """
        self.url_to_crawl = url_to_crawl

        super().__init__(**kwargs)

    def parse(self, response: Response, **kwargs):
        if self.url_to_crawl:
            yield response.follow(url=self.url_to_crawl, callback=self.parse_residences)
        else:
            residences = response.xpath("//div[@id='free_cart_holder']//a[contains(@class,'main_items item_cart')]/@href").getall()
            residences = list(set(residences))

            yield from response.follow_all(urls=residences, callback=self.parse_residences)

            next_page = response.xpath("//a[contains(.,'Pagina Următoare')]/@href").get()
            if next_page:
                yield response.follow(url=next_page, callback=self.parse)

    def parse_residences(self, response: Response):
        """
        @url https://homezz.ro/inchiriere-apartament-2-camere-mihai-bravu-2513627.html
        """
        loader = ResidenceItemLoader(selector=response)

        loader.add_xpath('price', "//span[@id='price']/text()", MapCompose(lambda s: s.replace('.', '')), re=r'[\d.]+')
        loader.add_xpath('currency', "//span[@id='price']/b/text()", MapCompose(lambda s: s.upper()))

        if any(map(str.isdigit, loader.get_output_value('price'))) and\
                not loader.get_output_value('price') or not 10 < float(loader.get_output_value('price')) < 10000:
            self.crawler.stats.inc_value('crawler/dropped_items')
            return

        if loader.get_output_value('currency') not in ['EUR', 'RON']:
            self.crawler.stats.inc_value('crawler/dropped_items')
            return

        loader.add_value('url', response.url)
        loader.add_xpath('zone', "//span[contains(.,'Zona')]/following-sibling::*//text()",
                         MapCompose(lambda s: s.lower()))
        loader.add_xpath('rooms', "//span[contains(.,'Număr camere')]/following-sibling::*//text()")
        loader.add_xpath('livable_area', "//span[contains(.,'Suprafața utilă')]/following-sibling::*//text()", re=r'\d+')
        loader.add_xpath('layout', "//span[contains(.,'Compartimentare')]/following-sibling::*//text()",
                         MapCompose(lambda s: s if s.lower().strip() in self.layout_mapping else None),
                         MapCompose(lambda s: self.layout_mapping.get(s.lower().strip())))
        loader.add_xpath('comfort', "//span[contains(.,'Confort')]/following-sibling::*//text()", re=r'\d')
        loader.add_xpath('floor', "//span[contains(.,'Etaj')]/following-sibling::*//text()", re=r'\d')
        loader.add_xpath('floors', "//span[contains(.,'Număr niveluri imobil')]/following-sibling::*//text()", re=r'\d')
        loader.add_xpath('building_year', "//span[contains(.,'An finalizare construcție')]/following-sibling::*//text()", re=r'\d{4}')
        loader.add_xpath('rooms', "//span[contains(.,'Număr Băi')]/following-sibling::*//text()")

        if self.url_to_crawl:
            print('Item crawled')

        yield loader.load_item()