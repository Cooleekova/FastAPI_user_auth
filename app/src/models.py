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


codes = Table(
    "codes", metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(50)),
    Column("reset_code", String(100)),
    Column("status", String(1)),
    Column("expired_in", DateTime)
)


blacklists = Table(
    "blacklist", metadata,
    Column("token", String(250), unique=True),
    Column("email", String(50)),
)


otps = Table(
    "otps", metadata,
    Column("id", Integer, primary_key=True),
    Column("recipient_id", String(100)),
    Column("session_id", String(100)),
    Column("otp_code", String(6)),
    Column("status", String(1)),
    Column("created_on", DateTime),
    Column("updated_on", DateTime),
    Column("otp_failed_count", Integer, default=0),
)


otp_blocks = Table(
    "otp_blocks", metadata,
    Column("id", Integer, primary_key=True),
     Column("recipient_id", String(100)),
    Column("created_on", DateTime),
)

