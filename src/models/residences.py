from sqlalchemy.dialects import mysql
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from conf.settings import MAX_PRICE, MIN_LIVABLE_AREA, MAX_LIVABLE_AREA, MAX_NR_ROOMS, MAX_PRICE_PER_SQ_METER, \
    RON_TO_EURO_CONVERSION_RATE, MIN_PRICE
from src.helpers.helpers import row_to_dict
from src.models import BaseTable, NotNullColumn


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

    def test_query(self):
        query = self.db_session.query(Residences).limit(50)

        return query.all()

    def get_residences(self, limit:int):
        if limit != -1:
            query = self.db_session.query(Residences).limit(limit)
        else:
            query = self.db_session.query(Residences)

        residences = self.clean_up_data(query.all())

        return residences

    def get_all_residences(self):
        return self.get_residences(-1)

    def clean_up_data(self, residences):
        residences_list = []

        for residence in residences:
            if residence.price and residence.livable_area \
                    and MAX_LIVABLE_AREA > residence.livable_area > MIN_LIVABLE_AREA and residence.rooms \
                    and residence.rooms < MAX_NR_ROOMS:
                res_dict = residence.__dict__
                if residence.currency == 'RON':
                    res_dict['price'] = int(residence.price / RON_TO_EURO_CONVERSION_RATE)
                if MIN_PRICE < residence.price < MAX_PRICE and residence.price / residence.livable_area < MAX_PRICE_PER_SQ_METER:
                    res_dict['livable_area'] = float(res_dict['livable_area'])
                    res_dict['built_area'] = float(res_dict['built_area']) if res_dict['built_area'] else None
                    residences_list.append(res_dict)

        return residences_list
