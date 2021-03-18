from sqlalchemy.dialects import mysql
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
import numpy as np
from conf.settings import MAX_PRICE, MIN_LIVABLE_AREA, MAX_LIVABLE_AREA, MAX_NR_ROOMS, MAX_PRICE_PER_SQ_METER, \
    RON_TO_EURO_CONVERSION_RATE, MIN_PRICE
from src.helpers.helpers import row_to_dict
from src.models import BaseTable, NotNullColumn
from src.models.ad_locations import AdLocations


class Residences(BaseTable):
    __tablename__ = 'residences'

    id = NotNullColumn(mysql.INTEGER, primary_key=True)
    main_ad_id = Column(mysql.VARCHAR, ForeignKey('ads.id'))
    price = Column(mysql.INTEGER)
    currency = Column(mysql.VARCHAR)
    location_id = Column(mysql.INTEGER, ForeignKey('ad_locations.id'))
    rooms = Column(mysql.SMALLINT)
    bathrooms = Column(mysql.SMALLINT)
    furnished = Column(mysql.SMALLINT)
    livable_area = Column(mysql.DECIMAL)
    floor = Column(mysql.SMALLINT)
    floors = Column(mysql.SMALLINT)
    building_year = Column(mysql.INTEGER)
    availability = Column(mysql.VARCHAR)
    balconies = Column(mysql.SMALLINT)
    balconies_closed = Column(mysql.TINYINT)
    built_area = Column(mysql.DECIMAL)
    comfort = Column(mysql.SMALLINT)
    conditioning = Column(mysql.VARCHAR)
    heating = Column(mysql.VARCHAR)
    layout = Column(mysql.SMALLINT)
    status = Column(mysql.SMALLINT)
    created_at = Column(mysql.DATETIME)

    # location = relationship('AdLocations', foreign_keys=[location_id])
    # ad = relationship('Ads', foreign_keys=[main_ad_id])

    list_of_desired_fields = []

    def test_query(self):
        query = self.db_session.query(Residences.id, AdLocations.zone_id).join(AdLocations).filter(AdLocations.zone_id).limit(50)

        return query.all()

    def get_residences(self, limit:int):
        if limit != -1:
            query = self.db_session.query(AdLocations.zone_id, Residences.price, Residences.currency, Residences.rooms,
                Residences.bathrooms, Residences.furnished, Residences.livable_area, Residences.floor, Residences.floors,
                Residences.building_year, Residences.balconies, Residences.balconies_closed, Residences.built_area,
                Residences.comfort, Residences.layout).join(AdLocations).filter(AdLocations.zone_id).limit(limit)
        else:
            query = self.db_session.query(AdLocations.zone_id, Residences.price, Residences.currency, Residences.rooms,
                                          Residences.bathrooms, Residences.furnished, Residences.livable_area,
                                          Residences.floor, Residences.floors,
                                          Residences.building_year, Residences.balconies, Residences.balconies_closed,
                                          Residences.built_area,
                                          Residences.comfort, Residences.layout).join(AdLocations).filter(
                AdLocations.zone_id).limit(limit)

        residences = self.clean_up_data(query.all())

        return residences

    def get_all_residences(self):
        return self.get_residences(-1)

    def clean_up_data(self, residences):
        residences_list = []

        for residence in residences:

            res_dict = {
                'balconies': residence.balconies,
                'balconies_closed': residence.balconies_closed,
                'bathrooms': residence.bathrooms,
                'built_area': residence.built_area,
                'livable_area': residence.livable_area,
                'comfort': residence.comfort,
                'currency': residence.currency,
                'floor': residence.floor,
                'floors': residence.floors,
                'furnished': residence.furnished,
                'layout': residence.layout,
                'price': residence.price,
                'rooms': residence.rooms,
                'zone_id': residence.zone_id,
                'building_year': residence.building_year
            }

            if res_dict['price'] \
                    and ((res_dict['livable_area'] and MAX_LIVABLE_AREA > res_dict['livable_area'] > MIN_LIVABLE_AREA) \
                    or (res_dict['built_area'] and MAX_LIVABLE_AREA > res_dict['built_area'] > MIN_LIVABLE_AREA))\
                    and res_dict['rooms'] and res_dict['rooms'] < MAX_NR_ROOMS:

                if res_dict['building_year']:
                    if res_dict['building_year'] > 2021 or 1900 < int(str(res_dict['building_year'])[:4]) < 2020:
                        res_dict['building_year'] = int(str(res_dict['building_year'])[:4])
                    else:
                        res_dict['building_year'] = np.nan
                if res_dict['currency'] == 'RON':
                    res_dict['price'] = int(res_dict['price'] / RON_TO_EURO_CONVERSION_RATE)
                if MIN_PRICE < res_dict['price'] < MAX_PRICE and res_dict['price'] / (res_dict['livable_area'] or res_dict['built_area']) < MAX_PRICE_PER_SQ_METER:
                    res_dict['livable_area'] = float(res_dict['livable_area']) if res_dict['livable_area'] else None
                    res_dict['built_area'] = float(res_dict['built_area']) if res_dict['built_area'] else None
                    residences_list.append(res_dict)

        return residences_list
