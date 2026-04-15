import datetime
import uuid
from fastapi import HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from crud.todo.todo import build_filter_conditions
from models import okr
from models.okr import Okr
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
    list_stmt = select(Okr)

    # 2. 定义允许的筛选字段白名单，防止非法字段注入
    allow_filter_keys = [
        'user_id',
        'program_id',
        'kr_name',
        'kr_desc',
        'status',
    ]
    # 3. 提取并处理分页参数
    # 获取页码，默认为 1
    page = query_params.get('page', 1)
    try:
        page = int(page)
        page = max(1, page)  # 保证页码至少为 1
    except (ValueError, TypeError):
        page = 1

    # 获取每页数量，默认为 10
    page_size = query_params.get('page_size', 10)
    try:
        page_size = int(page_size)
        # 限制最大每页数量，防止恶意请求过大导致数据库压力
        page_size = min(page_size, 100)
    except (ValueError, TypeError):
        page_size = 10

    # 计算偏移量 (offset = (页码 - 1) * 每页数量)
    offset = (page - 1) * page_size

    # 提取筛选条件
    filter_conditions = build_filter_conditions(Okr, allow_filter_keys, query_params)

    # 4. 如果有筛选条件，添加到查询语句中
    if filter_conditions:
        total_stmt = total_stmt.where(and_(*filter_conditions))
        list_stmt = list_stmt.where(and_(*filter_conditions))

    # 5. 分页
    list_stmt = list_stmt.offset(offset).limit(page_size)

    # 6. 执行数据库查询（异步执行）
    # 获取总数
    total_result = await db.execute(total_stmt)
    total = total_result.scalar() or 0  # 提取总数的标量值

    # 获取列表数据
    list_result = await db.execute(list_stmt)
    okr_list = list_result.scalars().all() or []
    # 7. 返回结果
    return total, okr_list


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
    stmt = select(Okr).where(Okr.id == okr_id)
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
    return await sql.update_by_id(db, okr.Okr, update_data.get('id'), update_data)


# 删除
async def delete_okr(
        okr_id: int,
        db: AsyncSession,
):
    return await sql.delete_by_id(db, okr.Okr, okr_id)
