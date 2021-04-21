from typing import Union

from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader

from crawler.webscraper.items import ResidenceItem

import re


def strip_and_remove_consecutive_spaces(s: str) -> Union[str, None]:
    def process(ss):
        return re.sub(r'\s+', ' ', ss).strip(' ,.;:\r\n')

    if isinstance(s, dict):
        for k, v in s.items():
            s[k] = strip_and_remove_consecutive_spaces(v)
    elif isinstance(s, list):
        s = [strip_and_remove_consecutive_spaces(v) for v in s]
    else:
        s = process(str(s))

    return s or None


def default_input(s: str) -> Union[str, None]:
    s = strip_and_remove_consecutive_spaces(s)

    if not s:
        return None

    blacklist = [
        'n/a',
        'n\\a',
        'undefined',
        '~',
        '-',
        'null',
        'not available',
        'other',
        '--',
        'none'
    ]

    for forbidden in blacklist:
        if forbidden == s.lower():
            return None

    return s


class ResidenceItemLoader(ItemLoader):
    default_item_class = ResidenceItem

    default_input_processor = MapCompose(default_input)
    default_output_processor = TakeFirst()
