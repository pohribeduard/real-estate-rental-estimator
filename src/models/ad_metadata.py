from sqlalchemy.dialects import mysql
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from src.models import BaseTable, NotNullColumn


class AdMetadata(BaseTable):
    __tablename__ = 'ad_metadata'

    id = NotNullColumn(mysql.INTEGER, primary_key=True)
    description = Column(mysql.VARCHAR, ForeignKey("counties.id"))

    def test_query(self):
        query = self.db_session.query(AdMetadata).limit(50)

        return query.all()
