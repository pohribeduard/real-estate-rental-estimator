from sqlalchemy.dialects import mysql

from src.models import NotNullColumn, BaseTable


class Counties(BaseTable):
    __tablename__ = 'counties'

    id = NotNullColumn(mysql.INTEGER, primary_key=True)
    name = NotNullColumn(mysql.VARCHAR)

    def test_query(self):
        query = self.db_session.query(Counties.id, Counties.name).limit(5)

        return query.all()
