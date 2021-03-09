from sqlalchemy.dialects import mysql
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from src.models import BaseTable, NotNullColumn


class Ads(BaseTable):
    __tablename__ = 'ads'

    id = NotNullColumn(mysql.INTEGER, primary_key=True)
    location_id = Column(mysql.INTEGER, ForeignKey('ad_locations.id'))
    ad_metadata_id = Column(mysql.INTEGER, ForeignKey('ad_metadata.id'))
    residence_id = Column(mysql.INTEGER, ForeignKey('residences.id'))
    appliances = Column(mysql.VARCHAR)
    availability = Column(mysql.VARCHAR)
    balconies = Column(mysql.SMALLINT)
    balconies_closed = Column(mysql.TINYINT)
    bathrooms = Column(mysql.SMALLINT)
    built_area = Column(mysql.DECIMAL)
    building_height = Column(mysql.DECIMAL)
    building_type = Column(mysql.SMALLINT)
    building_year = Column(mysql.INTEGER)
    commission = Column(mysql.DECIMAL)
    comfort = Column(mysql.SMALLINT)
    condition = Column(mysql.VARCHAR)
    conditioning = Column(mysql.VARCHAR)
    counters = Column(mysql.VARCHAR)
    currency = Column(mysql.VARCHAR)
    foundation_material = Column(mysql.VARCHAR)
    floor = Column(mysql.SMALLINT)
    floors = Column(mysql.SMALLINT)
    front_door = Column(mysql.VARCHAR)
    furnished = Column(mysql.SMALLINT)
    garages = Column(mysql.SMALLINT)
    general_utilities = Column(mysql.VARCHAR)
    heating = Column(mysql.VARCHAR)
    inside_doors = Column(mysql.VARCHAR)
    internet = Column(mysql.VARCHAR)
    kitchen = Column(mysql.VARCHAR)
    kitchens = Column(mysql.SMALLINT)
    layout = Column(mysql.SMALLINT)
    listed_date = Column(mysql.DATETIME)
    livable_area = Column(mysql.DECIMAL)
    parking_spots = Column(mysql.SMALLINT)
    price = Column(mysql.INTEGER)
    public_transportation = Column(mysql.TINYINT)
    rooms = Column(mysql.SMALLINT)
    original_id = Column(mysql.VARCHAR)
    services = Column(mysql.VARCHAR)
    status = Column(mysql.SMALLINT)
    street = Column(mysql.VARCHAR)
    street_lighting = Column(mysql.VARCHAR)
    title = Column(mysql.VARCHAR)
    type = Column(mysql.SMALLINT)
    thermal_insulation = Column(mysql.VARCHAR)
    url = Column(mysql.VARCHAR)
    walls = Column(mysql.VARCHAR)
    window_material = Column(mysql.VARCHAR)
    year = Column(mysql.SMALLINT)
    source = Column(mysql.VARCHAR)
    updated_at = Column(mysql.DATETIME)
    created_at = Column(mysql.DATETIME)

    # location = relationship('AdLocations', foreign_keys=[location_id])
    # ad_metadata = relationship('AdMetadata', foreign_keys=[ad_metadata_id])
    # ad_residence = relationship('Residences', foreign_keys=[residence_id])

    def test_query(self):
        query = self.db_session.query(Ads).limit(50)

        return query.all()
