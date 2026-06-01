import datetime
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, and_

from models.finance.income import Income, IncomeCate, IncomeSecondCate
from utils import sql


# 新增
async def add_income(
        add_data: dict,
        db: AsyncSession,
        user_id: int,
):
    new_income = Income(**add_data, user_id=user_id)
    db.add(new_income)
    await db.commit()
    await db.refresh(new_income)
    return new_income


# 条件查询列表-分页
async def query_income_list(
        db: AsyncSession,
        query_params: dict,
):
    # 1. 初始化总数查询和列表查询的基础语句（都限定当前用户）
    total_stmt = select(func.count(Income.id))
    list_stmt = select(Income).options(
        selectinload(Income.user),
        selectinload(Income.first_cate),
        selectinload(Income.second_cate),
        selectinload(Income.upload_images)
    )
    # 比较时间
    if query_params.get('start_date', None):
        total_stmt = total_stmt.where(Income.income_date >= query_params.get('start_date'))
        list_stmt = list_stmt.where(Income.income_date >= query_params.get('start_date'))
        query_params.pop('start_date')
    if query_params.get('end_date', None):
        total_stmt = total_stmt.where(Income.income_date <= query_params.get('end_date'))
        list_stmt = list_stmt.where(Income.income_date <= query_params.get('end_date'))
        query_params.pop('end_date')
    return await sql.common_query_list(db, query_params, total_stmt, list_stmt, Income)


# 根据id查询income
async def get_income_by_id(
        income_id: int,
        db: AsyncSession,
):
    """
    根据id查询income
    :param income_id:
    :param db:
    :return:
    """
    stmt = select(Income).options(
        selectinload(Income.upload_images),
        selectinload(Income.user),
    ).where(Income.id == income_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_income_by_okr_id(
        okr_id: int,
        db: AsyncSession,
):
    """
    根据id查询expense
    :param okr_id:
    :param db:
    :return:
    """
    stmt = select(Income).where(Income.okr_id == okr_id)
    result = await db.execute(stmt)
    return result.scalars().all()

# 更新
async def update_income(
        update_data: dict,
        db: AsyncSession,
):
    # 先看incomeId是否存在。
    income = await get_income_by_id(int(update_data['id']), db)
    if not income:
        return None
    # 3. 更新对象的属性
    # 遍历 update_data 中的键值对，排除掉 id (通常主键不更新)
    for key, value in update_data.items():
        if key != 'id' and hasattr(income, key):
            setattr(income, key, value)
    await db.commit()
    await db.refresh(income)
    return income


# 删除
async def delete_income(
        income_id: int,
        db: AsyncSession,
):
    stmt = delete(Income).where(Income.id == income_id)
    await db.execute(stmt)
    await db.commit()
    return True


# 获取总数
async def get_total_list(db: AsyncSession,
                         user_id: int):
    """
    获取某用户的Income总数
    :param db:
    :param user_id:
    :return:
    """
    return await sql.get_total_list(db, user_id, Income)
