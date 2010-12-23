import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class MyDataModel(Base):
    __tablename__ = 'academe_mydata'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
