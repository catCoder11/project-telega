import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class K_corpus(SqlAlchemyBase):
    __tablename__ = 'corpuses'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modify_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    klass_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("klasses.id"), nullable=True)
    klass = orm.relationship('K_klass')
    auditory = orm.relationship("K_auditory", back_populates='corpus')
    # school_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"), nullable=True)
    # school = orm.relationship('K_school')


class K_access_type(SqlAlchemyBase):
    __tablename__ = 'access_type'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    access = orm.relationship("Access", back_populates='access_type')

class K_auditory(SqlAlchemyBase):
    __tablename__ = 'auditory'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modify_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    corpus_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("corpuses.id"), nullable=True)
    corpus = orm.relationship('K_corpus')
    rasp = orm.relationship("Rasp", back_populates='auditory')




# class K_school(SqlAlchemyBase):
#     __tablename__ = 'schools'
#     id = sqlalchemy.Column(sqlalchemy.Integer,
#                            primary_key=True, autoincrement=True)
#     name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
#     modify_date = sqlalchemy.Column(sqlalchemy.DateTime,
#                                      default=datetime.datetime.now)
#     creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
#     corpus = orm.relationship("K_corpus", back_populates='school')


class K_klass(SqlAlchemyBase):
    __tablename__ = 'klasses'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    class_key = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, unique=True, index=True)
    modify_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    corpus = orm.relationship("K_corpus", back_populates='klass')
    access = orm.relationship("Access", back_populates='klass')
    rasp = orm.relationship("Rasp", back_populates='klass')
    teachers = orm.relationship("K_teacher", back_populates='klass')


class K_subject(SqlAlchemyBase):
    __tablename__ = 'subjects'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modify_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    rasp = orm.relationship("Rasp", back_populates='subject')

class K_teacher(SqlAlchemyBase):
    __tablename__ = 'teachers'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    fio = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modify_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    klass_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("klasses.id"), nullable=True)
    klass = orm.relationship("K_klass")
    rasp = orm.relationship("Rasp", back_populates='teacher')


class K_task_type(SqlAlchemyBase):
    __tablename__ = 'task_types'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modify_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    task = orm.relationship('Tasks', back_populates='task_type')

class K_file_to_task(SqlAlchemyBase):
    __tablename__ = 'f_to_t'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tasks.id"), nullable=True)
    task = orm.relationship('Tasks')
    file_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("files.id"), nullable=True)
    file = orm.relationship('File')
