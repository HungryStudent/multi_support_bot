from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger, Table, VARCHAR, TIMESTAMP, SMALLINT
from sqlalchemy.orm import relationship

from .database import Base


class Users(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True)
    username = Column(VARCHAR(32))
    reg_time = Column(TIMESTAMP)


class Bots(Base):
    __tablename__ = "bots"

    bot_id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(50))
    api_token = Column(VARCHAR(50))
    manager_id = Column(BigInteger)
    owner_id = Column(BigInteger, ForeignKey(Users.user_id))
    hello_msg = Column(VARCHAR(3000))


class BannedUsers(Base):
    __tablename__ = "banned_users"

    id = Column(Integer, primary_key=True, index=True)
    bot_id = Column(BigInteger)
    user_id = Column(BigInteger)


class Questions(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    bot_id = Column(BigInteger, ForeignKey(Bots.bot_id, ondelete="CASCADE"))
    user_id = Column(BigInteger)
    msg_id = Column(Integer)
    ques = Column(VARCHAR(4096))
    ans = Column(VARCHAR(4096))
    create_time = Column(TIMESTAMP)
