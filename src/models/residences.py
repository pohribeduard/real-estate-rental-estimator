from sqlalchemy.dialects import mysql
from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.orm import relationship
import numpy as np
from conf.settings import MAX_PRICE, MIN_LIVABLE_AREA, MAX_LIVABLE_AREA, MAX_NR_ROOMS, MAX_PRICE_PER_SQ_METER, \
    RON_TO_EURO_CONVERSION_RATE, MIN_PRICE
from src.helpers.helpers import row_to_dict
from src.models import BaseTable, NotNullColumn
from src.models.ad_locations import AdLocations
from src.models.zones import Zones
from src.validators.residence_validator import ResidenceValidator


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

    def get_all_residences(self):
        return self.get_residences(-1)

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
                AdLocations.zone_id)

        residences = self.format_residences(query.all())

        return residences

    def get_zones(self):
        query = self.db_session.query(AdLocations.zone_id, Zones.name).select_from(Residences).join(AdLocations)\
            .join(Zones).group_by(AdLocations.zone_id).having(func.count(AdLocations.zone_id) > 100)\
            .order_by(Zones.name)

        zones = self.format_zones(query.all())

        return zones

    def format_zones(self, zones_results):
        zones_list = []

        for zone in zones_results:
            zone_dict = {
                'zone_id': zone.zone_id,
                'name': zone.name.title()
            }
            zones_list.append(zone_dict)

        return zones_list

    def format_residences(self, residences):
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

            res_dict = ResidenceValidator().clean_up_residences(res_dict)
            if res_dict:
                #   TODO: decide pe care sa o folosesti
                res_dict['price_interval'] = res_dict['price'] / 50
                # res_dict['price_interval'] = res_dict['price'] // 50
                residences_list.append(res_dict)

        return residences_list





