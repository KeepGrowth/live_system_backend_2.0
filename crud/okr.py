import datetime
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from models import okr
from models.okr import Okr
from models.program import Program
from utils import security, sql


# 新增
async def add_okr(
        add_data: dict,
        db: AsyncSession,
):
    new_okr = okr.Okr(**add_data)
    db.add(new_okr)
    await db.commit()
    await db.refresh(new_okr)
    return new_okr


# 分页查询
async def query_okr_list(
        db: AsyncSession,
        query_params: dict
):
    """
    分页查询OKR数据列表。
    :param db:
    :param query_params:
    :return:
    """
    # 1. 初始化总数查询和列表查询的基础语句（都限定当前用户）
    total_stmt = select(func.count(Okr.id))
    list_stmt = select(Okr).options(
        selectinload(Okr.upload_images),
        selectinload(Okr.todo_logs),
        selectinload(Okr.todos),
        selectinload(Okr.program),
        selectinload(Okr.goal),
        selectinload(Okr.user),
    )
    return await sql.common_query_list(db, query_params, total_stmt, list_stmt, Okr)


# 根据项目id查询
async def get_okr_list_by_program_id(
        db: AsyncSession,
        program_id: int
):
    list_stmt = select(Okr).options(
        selectinload(Okr.program),
        selectinload(Okr.goal)
    ).where(Okr.program_id == program_id)
    result = await db.execute(list_stmt)
    return result.scalars().all()


# 级联查询
async def query_okr_cascade_list(
        db: AsyncSession,
        user_id: int
):
    """
    年份→项目→OKR
    :param db:
    :param user_id:
    :return:
    """
    stmt = (
        select(
            Okr.id,
            Okr.program_id,
            Okr.kr_name,
            Okr.create_time,
            Program.program_name,
        )
        .join(Okr.program)  # 通过关系进行连接
        .where(Okr.user_id == user_id)
        .order_by(Okr.create_time.desc())
    )
    result = await db.execute(stmt)
    return result.mappings().all()


# 根据id查询
async def get_okr_by_id(
        db: AsyncSession,
        okr_id: int
):
    """
    根据id查询OKR数据。
    :param db:
    :param okr_id:
    :return:
    """
    stmt = (select(Okr).options(
        selectinload(Okr.user),
        selectinload(Okr.program),
        selectinload(Okr.goal),
        selectinload(Okr.upload_images),
    )
            .where(Okr.id == okr_id))
    target_okr = await db.execute(stmt)
    return target_okr.scalar_one_or_none()


# 更新
async def update_okr(
        update_data: dict,
        db: AsyncSession,
):
    target_okr = await get_okr_by_id(db, update_data.get('id'))
    if not target_okr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未找到该OKR')
    # 3. 更新对象的属性
    # 遍历 update_data 中的键值对，排除掉 id (通常主键不更新)
    for key, value in update_data.items():
        if key != 'id' and hasattr(target_okr, key):
            setattr(target_okr, key, value)
    await db.commit()
    await db.refresh(target_okr)
    return target_okr


# 删除
async def delete_okr(
        okr_id: int,
        db: AsyncSession,
):
    return await sql.delete_by_id(db, okr.Okr, okr_id)


# 获取总数
async def get_total_list(db: AsyncSession,
                         user_id: int):
    """
    获取某用户的OKR总数
    :param db:
    :param user_id:
    :return:
    """
    return await sql.get_total_list(db, user_id, Okr)
