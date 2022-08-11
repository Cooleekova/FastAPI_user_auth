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



 # Column("id", Integer, Sequence("user_id_seq"), primary_key=True),



#class User(Base):
    ##id = Column(Integer,primary_key=True,index=True)
   # username = Column(String,unique=True,nullable=False)
   # email = Column(String,nullable=False,unique=True,index=True)
  #  hashed_password = Column(String,nullable=False)
  #  is_active = Column(Boolean(),default=True)
  #  is_superuser = Column(Boolean(),default=False)
  #  jobs = relationship("Job",back_populates="owner")
    