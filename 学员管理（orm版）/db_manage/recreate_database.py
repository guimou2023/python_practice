from sqlalchemy.orm import sessionmaker
from core.init_db import engine

session = sessionmaker(bind=engine)()
session.execute('drop database if exists stu_db;create database stu_db charset utf8;')

