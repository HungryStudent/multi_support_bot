from typing import List

from pydantic import parse_obj_as
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func, text
from sqlalchemy import func
from core import models, schemas
import random
import string

import hashlib

from core.database import SessionLocal


def get_db():
    db = SessionLocal()
    return db


def add_user(user_data: schemas.UserCreate):
    with get_db() as db:
        user = models.Users(**user_data.dict())
        db.add(user)
        db.commit()


def get_user(user_id) -> schemas.UserOut:
    with get_db() as db:
        return db.query(models.Users).filter(models.Users.user_id == user_id).first()


def add_bot(bot_data: schemas.BotCreate):
    with get_db() as db:
        dop_bot = models.Bots(**bot_data.dict())
        try:
            db.add(dop_bot)
            db.commit()
        except IntegrityError:
            pass


# Таблица с ботами
def get_bots() -> List[schemas.BotOut]:
    with get_db() as db:
        return db.query(models.Bots).all()


def get_bots_by_user_id(user_id) -> List[schemas.BotOut]:
    with get_db() as db:
        result = db.query(models.Bots, func.count(models.Questions.bot_id).filter(models.Questions.ans.is_(None)).label(
            "ques_count")).group_by(models.Bots.bot_id).filter(models.Bots.owner_id == user_id).all()
        res = []
        for bot, count in result:
            res.append(
                schemas.BotOut(bot_id=bot.bot_id, manager_id=bot.manager_id, name=bot.name,
                               api_token=bot.api_token, ques_count=count, owner_id=bot.owner_id, hello_msg=bot.hello_msg))
        return res


def get_bot_by_token(token) -> schemas.BotOut:
    with get_db() as db:
        db.close()
        return db.query(models.Bots).filter(models.Bots.api_token == token).first()


def get_bot(bot_id) -> schemas.BotOut:
    with get_db() as db:
        return db.query(models.Bots).filter(models.Bots.bot_id == bot_id).first()


def change_hello_msg(new_text, bot_id):
    with get_db() as db:
        db.query(models.Bots).filter(models.Bots.bot_id == bot_id).update({"hello_msg": new_text})
        db.commit()


def delete_bot(bot_id):
    with get_db() as db:
        db.query(models.Bots).filter(models.Bots.bot_id == bot_id).delete()
        db.commit()


def set_bot_manager_id(api_token, manager_id):
    with get_db() as db:
        db.query(models.Bots).filter(models.Bots.api_token == api_token).update({"manager_id": manager_id})
        db.commit()


def add_ques(ques_data: schemas.QuestionCreate):
    with get_db() as db:
        ques = models.Questions(**ques_data.dict())
        db.add(ques)
        db.commit()
        return db.query(models.Bots.manager_id).filter(models.Bots.bot_id == ques_data.bot_id).first()


def get_stat():
    with get_db() as db:
        stat_data = [0, 0]
        stat_data[0] = db.query(func.count(models.Users.user_id)).first()[0]
        stat_data[1] = db.query(func.count(models.Bots.bot_id)).first()[0]
        return stat_data


def ban_user(bot_id, user_id):
    with get_db() as db:
        banned_user = models.BannedUsers(bot_id=bot_id, user_id=user_id)
        db.add(banned_user)
        db.commit()


def unban_user(bot_id, user_id):
    with get_db() as db:
        db.query(models.BannedUsers).where(models.BannedUsers.bot_id == bot_id,
                                           models.BannedUsers.user_id == user_id).delete()
        db.commit()


def get_banned_user(bot_id, user_id):
    with get_db() as db:
        return db.query(models.BannedUsers).where(models.BannedUsers.bot_id == bot_id,
                                                  models.BannedUsers.user_id == user_id).first()
