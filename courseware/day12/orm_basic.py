__author__ = "Alex Li"

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Enum,DATE,Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:alex3714@192.168.16.86/oldboydb",
                       encoding='utf-8')

Base = declarative_base()  # 生成orm基类
class User(Base):
    __tablename__ = 'user'  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(64))

    def __repr__(self):
        return  "<%s name:%s>" % (self.id,self.name)

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    name = Column(String(32),nullable=False)
    register_date = Column(DATE,nullable=False)
    gender = Column(String(32),nullable=False)


    def __repr__(self):
        return "<%s name:%s>" % (self.id, self.name)
Base.metadata.create_all(engine)  # 创建表结构

Session_class = sessionmaker(bind=engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
Session = Session_class()  # 生成session实例 #cursor

# user_obj = User(name="alex", password="alex3714")  # 生成你要创建的数据对象
# user_obj2 = User(name="jack", password="122")  # 生成你要创建的数据对象
# print(user_obj.name, user_obj.id)  # 此时还没创建对象呢，不信你打印一下id发现还是None
# Session.add(user_obj)  # 把要创建的数据对象添加到这个session里， 一会统一创建
# Session.add(user_obj2)  # 把要创建的数据对象添加到这个session里， 一会统一创建
#
# print(user_obj.name, user_obj.id)  # 此时也依然还没创建



# data = Session.query(User).filter(User.id >1).filter(User.id <4 ).first()
# # print(dir(Session))
# # data.name = "Jack Liu"
# # data.password = "Shit happens"
#
# fake_user = User(name='Rain', password='12345')
# Session.add(fake_user)

# print(Session.query(User).filter(User.name.in_(['alex', 'rain'])).count())  # 这时看session里有你刚添加和修改的数据

# Session.rollback()  # 此时你rollback一下
# print("after rollback")
# print(Session.query(User).filter(User.name.in_(['Jack', 'rain'])).all())  # 这时看session里有你刚添加和修改的数据
#
from sqlalchemy import func

# print(Session.query( User.name,func.count(User.name)).group_by(User.name).all())
# Session.commit()  # 现此才统一提交，创建数据

# s1 = Student(name="s2",register_date="2015-03-01",gender="F")
# Session.add(s1)
# print(Session.query(User,Student).filter(User.id==Student.id).all())
print(Session.query(User).join(Student,isouter=True).all())
Session.commit()