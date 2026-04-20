"""
项目完成日志增删改查。
"""
import datetime
import uuid
from fastapi import HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.program import Program, ProgramLog
from utils import security, sql


# 获取总数
async def get_total_num(db: AsyncSession,
                        user_id: int):
    """
    获取某用户的项目日志总数
    :param db:
    :param user_id:
    :return:
    """
    return sql.get_total_list(db, user_id, ProgramLog)
