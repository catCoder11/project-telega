import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class File(SqlAlchemyBase):
    __tablename__ = 'files'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    file = sqlalchemy.Column(sqlalchemy.BLOB)
    modify_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    f_to_t = orm.relationship('K_file_to _task', back_populates='file')