from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, Sequence, Boolean, ForeignKey
from sqlalchemy.orm import relationship
#from db.base_class import Base

metadata = MetaData()

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(50)),
    Column("password", String(200)),
    Column("fullname", String(50)),
    Column("created_on", DateTime),
    Column("status", String(1)),
)


codes = Table(
    "codes", metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(50)),
    Column("reset_code", String(100)),
    Column("status", String(1)),
    Column("expired_in", DateTime)
)

 # Column("id", Integer, Sequence("user_id_seq"), primary_key=True),

    