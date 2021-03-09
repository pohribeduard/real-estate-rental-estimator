from sqlalchemy.dialects import mysql
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from src.models import BaseTable, NotNullColumn


class Zones(BaseTable):
    __tablename__ = 'zones'

    id = NotNullColumn(mysql.INTEGER, primary_key=True)
    city_id = Column(mysql.INTEGER, ForeignKey('cities.id'))
    name = Column(mysql.VARCHAR)
    latitude = Column(mysql.DECIMAL)
    longitude = Column(mysql.DECIMAL)
    created_at = Column(mysql.DATETIME)

    # city = relationship('Cities')

    def test_query(self):
        query = self.db_session.query(Zones).limit(50)

        return query.all()
