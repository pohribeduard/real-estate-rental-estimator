from sqlalchemy.dialects import mysql
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from src.models import BaseTable, NotNullColumn


class Cities(BaseTable):
    __tablename__ = 'cities'

    id = NotNullColumn(mysql.INTEGER, primary_key=True)
    county_id = Column(mysql.INTEGER, ForeignKey('counties.id'))
    name = Column(mysql.VARCHAR)
    latitude = Column(mysql.DECIMAL)
    longitude = Column(mysql.DECIMAL)

    county = relationship('Counties')

    def test_query(self):
        query = self.db_session.query(Cities).limit(50)

        return query.all()