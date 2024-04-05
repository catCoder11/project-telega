import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Access(SqlAlchemyBase):
    __tablename__ = 'acesses'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    modify_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime)
    creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    telegram_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.telegram_id"), nullable=True)
    user = orm.relationship('User')
    klass_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("klasses.id"), nullable=True)
    klass = orm.relationship('K_klass')
    access_type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("access_type.id"), nullable=True)
    access_type = orm.relationship('K_access_type')
