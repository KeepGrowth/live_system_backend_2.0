import datetime
import uuid
from fastapi import HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models import okr
from utils import security, sql


# 新增
async def add_okr(
        add_data: dict,
        db: AsyncSession,
        user_id: int,
):
    new_okr = okr.Okr(**add_data, user_id=user_id)
    db.add(new_okr)
    await db.commit()
    await db.refresh(new_okr)
    return new_okr


# 获取列表
async def get_okr_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10,
):
    return await sql.get_list_by_user_id(db, okr.Okr, user_id, page, page_size)


# 更新
async def update_okr(
        update_data: dict,
        db: AsyncSession,
):
    return await sql.update_by_id(db, okr.Okr, update_data['id'], update_data)


# 删除
async def delete_okr(
        okr_id: int,
        db: AsyncSession,
):
    return await sql.delete_by_id(db, okr.Okr, okr_id)
