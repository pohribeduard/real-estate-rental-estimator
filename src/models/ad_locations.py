from sqlalchemy.dialects import mysql
from sqlalchemy import Column, ForeignKey
from src.models import NotNullColumn, BaseTable
from sqlalchemy.orm import relationship


class AdLocations(BaseTable):
    __tablename__ = 'ad_locations'

    id = NotNullColumn(mysql.INTEGER, primary_key=True)
    zone_id = Column(mysql.INTEGER, ForeignKey('zones.id'))
    address = Column(mysql.VARCHAR)
    hash = Column(mysql.CHAR)   #TODO: ce e asta?
    latitude = Column(mysql.DECIMAL)
    longitude = Column(mysql.DECIMAL)
    created_at = Column(mysql.DATETIME)

    # zone = relationship('Zones')

    def test_query(self):
        query = self.db_session.query(AdLocations).limit(500)

        return query.all()

