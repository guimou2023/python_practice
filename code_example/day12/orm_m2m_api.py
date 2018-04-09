__author__ = "Alex Li"
from day12 import orm_m2m
from sqlalchemy.orm import sessionmaker

Session_class = sessionmaker(bind=orm_m2m.engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
session = Session_class()  # 生成session实例 #cursor

#
# b1 = orm_m2m.Book(name="learn python with Alex",pub_date="2014-05-2")
# b2= orm_m2m.Book(name="learn Zhangbility with Alex",pub_date="2015-05-2")
b3 = orm_m2m.Book(name="跟Alex去泰国",pub_date="2016-05-2")

# a1 = orm_m2m.Author(name="Alex")
# a2 = orm_m2m.Author(name="Jack")
# a3 = orm_m2m.Author(name="Rain")
#
# b1.authors = [a1,a3]
# b3.authors = [a1,a2,a3]
#
session.add_all([b3,])

# author_obj = session.query(orm_m2m.Author).filter(orm_m2m.Author.name=="alex").first()
# print(author_obj)
# book_obj = session.query(orm_m2m.Book).filter(orm_m2m.Book.id==2).first()
# book_obj.authors.remove(author_obj)
session.commit()