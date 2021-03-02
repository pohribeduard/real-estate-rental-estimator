from sqlalchemy.dialects import mysql
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

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
    layout = Column(mysql.SMALLINT) # TODO: ce e asta?
    status = Column(mysql.SMALLINT)
    created_at = Column(mysql.DATETIME)

    location = relationship('AdLocations', foreign_keys=[location_id])
    ad = relationship('Ads', foreign_keys=[main_ad_id])

    def test_query(self):
        query = self.db_session.query(Residences).limit(50)

        return query.all()
