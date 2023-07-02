from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker

from __init__ import admins, Base, engine
from .table import user, user_2, admin, basket, reviews 


Session = sessionmaker(bind=engine)

session = Session()

class User(Base):

  __tablename__ = 'user'

  id = Column(Integer, primary_key=True)
  id_user = Column(String(100))
  name_user = Column(String(100))

  def __init__(self, id_user, name_user):
     self.id_user = id_user
     self.name_user = name_user
  

class User_2(Base):
  
  __tablename__ = 'user_2'

  id = Column(Integer, primary_key=True)
  id_user = Column(String(100))
  name_user = Column(String(100))
  types = Column(String(50))
  description = Column(String(500))

  def __init__(self, id_user, name_user, types, description):
     self.id_user = id_user
     self.name_user = name_user
     self.types = types
     self.description = description
  

class Reviews(Base):

  __tablename__ = 'reviews'

  id = Column(Integer, primary_key=True)
  id_user = Column(String(100))
  name_user = Column(String(100))
  reviews = Column(String(500))

  def __init__(self, id_user, name_user, reviews):
     self.id_user = id_user
     self.name_user = name_user
     self.reviews = reviews
  

class Admin(Base):

  __tablename__ = 'admin'

  id = Column(Integer, primary_key=True)
  id_user = Column(String(100))
  name_user = Column(String(100))

  def __init__(self, id_user, name_user):
     self.id_user = id_user
     self.name_user = name_user

class Basket(Base):

  __tablename__ = 'basket'

  id = Column(Integer, primary_key=True)
  id_user = Column(String(100))
  name_user = Column(String(100))
  types = Column(String(100))
  name = Column(String(100))
  price = Column(String(100))

  def __init__(self, id_user, name_user, types, price):
     self.id_user = id_user
     self.name_user = name_user
     self.types = types
     self.price = price
  

def update_count_offers(id_to_update, new_desc):
    try:
        query = session.query(User).filter(User.id_user == id_to_update).\
            update({User.count_offers: new_desc}, synchronize_session=False)
        session.commit()
    except:
        session.rollback()

def creates(what):
  try:
    what.create(engine)

    if what == admin:
       for i in list(admins.values()):
        admin_commit = Admin(i['id_user'], i['name'])
        
        session.add(admin_commit)
        session.commit()
        session.close()
  except:
     pass

table = [admin, user, reviews, user_2, basket]

for i in table:
    creates(i)