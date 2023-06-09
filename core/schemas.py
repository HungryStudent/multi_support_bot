from typing import List, Union
from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    user_id: int
    username: str = None
    reg_time: datetime


class UserOut(BaseModel):
    user_id: int
    username: str = None
    reg_time: datetime


class BotCreate(BaseModel):
    bot_id = int
    name: str
    api_token: str
    owner_id: int
    hello_msg: str


class BotOut(BaseModel):
    bot_id: int
    name: str
    api_token: str
    manager_id: int = None
    owner_id: int
    hello_msg: str
    ques_count: int


class QuestionCreate(BaseModel):
    bot_id: int
    user_id: int
    msg_id: int
    ques: str = None
    create_time: datetime
