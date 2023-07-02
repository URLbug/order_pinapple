from sqlalchemy import Column, String, Integer, Table

from __init__ import metadata_obj


user = Table(
  "user",
  metadata_obj,
  Column("id", Integer, primary_key=True),
  Column("id_user", String(100)),
  Column("name_user", String(100)),
)

user_2 = Table(
  "user_2",
  metadata_obj,
  Column("id", Integer, primary_key=True),
  Column("id_user", String(100)),
  Column("name_user", String(100)),
  Column("types", String(50)),
  Column("description", String(500))
)

reviews = Table(
  "reviews",
  metadata_obj,
  Column("id", Integer, primary_key=True),
  Column("id_user", String(100)),
  Column("name_user", String(100)),
  Column("reviews", String(500))
)

admin = Table(
    "admin",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("id_user", String(100)),
    Column("name_user", String(100)),
)

basket = Table(
   'basket',
   metadata_obj,
   Column("id", Integer, primary_key=True),
   Column("id_user", String(100)),
   Column("name_user", String(100)),
   Column('name', String(100)),
   Column('types', String(100)),
   Column('price', String(100))
)