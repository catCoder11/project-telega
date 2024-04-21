import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Rasp(SqlAlchemyBase):
    __tablename__ = 'rasp'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    modify_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    klass_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("klasses.id"), nullable=True)
    klass = orm.relationship('K_klass')
    auditory_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("auditory.id"), nullable=True)
    auditory = orm.relationship('K_auditory')
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subjects.id"), nullable=True)
    subject = orm.relationship('K_subject')
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teachers.id"), nullable=True)
    teacher = orm.relationship('K_teacher')
    task = orm.relationship('Tasks', back_populates="rasp")
    # rasp_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("rasp.id"), nullable=True)
    # rasp = orm.relationship('Rasp')
    # task_type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("rasp.id"), nullable=True)
    # task_type = orm.relationship('K_task_type')
    # descriptions = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # modify_date = sqlalchemy.Column(sqlalchemy.DateTime,
    #                                  default=datetime.datetime.now)
    # creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # f_to_t = orm.relationship('K_file_to_task', back_populates='task')
