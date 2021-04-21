import scrapy
from itemloaders.processors import MapCompose
from scrapy.http import Response

from crawler.webscraper.itemloaders import ResidenceItemLoader


class Imobiliare(scrapy.Spider):
    name = 'imobiliare.ro'
    allowed_domains = [
        'imobiliare.ro'
    ]

    start_urls = [
        'https://www.imobiliare.ro/inchirieri-apartamente/bucuresti-ilfov?id=128177126'
    ]

    def parse(self, response: Response, **kwargs):
        residences = response.xpath("//a[contains(@class,'detalii-proprietate')][contains(.,'Vezi detalii')]/@href").getall()
        residences = list(set(residences))

        yield from response.follow_all(urls=residences, callback=self.parse_residences)

        next_page = response.xpath("//a[@class='inainte butonpaginare']/@href").get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)

    def parse_residences(self, response: Response):
        """
        @url https://www.imobiliare.ro/inchirieri-apartamente/bucuresti/universitate/apartament-de-inchiriat-2-camere-XV0L00ICA

        """
        loader = ResidenceItemLoader(selector=response)

        loader.add_xpath('price', "//div[contains(@itemprop,'price')]/text()", MapCompose(lambda s: s.replace('.', '')))

        if not loader.get_output_value('price') or not 10 < float(loader.get_output_value('price')) < 10000:
            return

        loader.add_value('url', response.url)

        loader.add_xpath('rooms', "//li[contains(.,'Nr. camere')]/span/text()")
        loader.add_xpath('livable_area', "//li[contains(.,'Suprafaţă utilă')]/span/text()", re=r'\d+')
        loader.add_xpath('built_area', "//li[contains(.,'Suprafaţă construită')]/span/text()", re=r'\d+')
        loader.add_xpath('layout', "//li[contains(.,'Compartimentare')]/span/text()") #TODO: map this
        loader.add_xpath('comfort', "//li[contains(.,'Confort')]/span/text()", re=r'\d')
        loader.add_xpath('floor', "//li[contains(.,'Etaj')]/span/text()", re=r'(\d+).?\/')
        loader.add_xpath('floors', "//li[contains(.,'Etaj')]/span/text()", re=r'\/.?(\d+)')
        loader.add_xpath('bathrooms', "//li[contains(.,'Nr. băi')]/span/text()")
        loader.add_xpath('balconies', "//li[contains(.,'Nr. balcoane')]/span/text()")
        loader.add_xpath('building_year', "//li[contains(.,'An construcţie')]/span/text()", re=r'\d{4}')
        loader.add_xpath('rooms', "//li[contains(.,'Nr. camere')]/span/text()")
        loader.add_xpath('currency', "//div[contains(@itemprop,'price')]/div/p/text()")
        loader.add_xpath('zone', "//div[@class='container-breadcrumbs']/ul[1]/li[last()]/a/@href",
                         MapCompose(lambda s: s.replace('-', ' ')), re=r'bucuresti/(.+)$')
        #balconies_closed

        yield loader.load_item()
