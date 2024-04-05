import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Tasks(SqlAlchemyBase):
    __tablename__ = 'tasks'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    rasp_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("rasp.id"), nullable=True)
    rasp = orm.relationship('Rasp')
    task_type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("task_types.id"), nullable=True)
    task_type = orm.relationship('K_task_type')
    descriptions = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modify_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    f_to_t = orm.relationship('K_file_to_task', back_populates='task')