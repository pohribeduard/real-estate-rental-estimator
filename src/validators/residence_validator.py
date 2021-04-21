from conf.settings import RON_TO_EURO_CONVERSION_RATE, MAX_PRICE, MIN_PRICE, MIN_LIVABLE_AREA, MAX_LIVABLE_AREA, \
    MAX_PRICE_PER_SQ_METER, MAX_NR_ROOMS, MIN_PRICE_PER_SQ_METER
import numpy as np


class ResidenceValidator:
    def __init__(self):
        pass

    def clean_up_residences(self, residence):
        if not residence['price']:
            return None

        if residence['currency'] == 'RON':
            residence['price'] = int(residence['price'] / RON_TO_EURO_CONVERSION_RATE)

        if not MIN_PRICE < residence['price'] < MAX_PRICE:
            return None

        if not residence['livable_area'] and not residence['built_area']:
            return None

        if residence['livable_area']:
            if not MIN_LIVABLE_AREA < residence['livable_area'] < MAX_LIVABLE_AREA:
                return None

            if not MIN_PRICE_PER_SQ_METER < residence['price'] / residence['livable_area'] < MAX_PRICE_PER_SQ_METER:
                return None

            residence['livable_area'] = float(residence['livable_area'])

        if residence['built_area']:
            if not MIN_LIVABLE_AREA < residence['built_area'] < MAX_LIVABLE_AREA:
                return None

            if not MIN_PRICE_PER_SQ_METER < residence['price'] / residence['built_area'] < MAX_PRICE_PER_SQ_METER:
                return None

            residence['built_area'] = float(residence['built_area'])

        if residence['rooms']:
            if residence['rooms'] > MAX_NR_ROOMS:
                return None

        if residence['building_year']:
            if residence['building_year'] > 2021 or 1900 < int(str(residence['building_year'])[:4]) < 2020:
                residence['building_year'] = int(str(residence['building_year'])[:4])
            else:
                residence['building_year'] = np.nan

        return residence
