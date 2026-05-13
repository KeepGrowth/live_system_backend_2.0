import datetime
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, and_

from models.finance.expense import Expense, ExpenseCate, ExpenseSecondCate
from utils import sql


# 新增
async def add_expense(
        add_data: dict,
        db: AsyncSession,
        user_id: int,
):
    new_expense = Expense(**add_data, user_id=user_id)
    db.add(new_expense)
    await db.commit()
    await db.refresh(new_expense)
    return new_expense


# 条件查询列表-分页
async def query_expense_list(
        db: AsyncSession,
        query_params: dict,
):
    # 1. 初始化总数查询和列表查询的基础语句（都限定当前用户）
    total_stmt = select(func.count(Expense.id))
    list_stmt = select(Expense).options(
        selectinload(Expense.user),
        selectinload(Expense.first_cate),
        selectinload(Expense.second_cate),
        selectinload(Expense.upload_images)
    )
    # 比较时间
    if query_params.get('start_date', None):
        total_stmt = total_stmt.where(Expense.expense_date >= query_params.get('start_date'))
        list_stmt = list_stmt.where(Expense.expense_date >= query_params.get('start_date'))
        query_params.pop('start_date')
    if query_params.get('end_date', None):
        total_stmt = total_stmt.where(Expense.expense_date <= query_params.get('end_date'))
        list_stmt = list_stmt.where(Expense.expense_date <= query_params.get('end_date'))
        query_params.pop('end_date')
    return await sql.common_query_list(db, query_params, total_stmt, list_stmt, Expense)


# 根据id查询expense
async def get_expense_by_id(
        expense_id: int,
        db: AsyncSession,
):
    """
    根据id查询expense
    :param expense_id:
    :param db:
    :return:
    """
    stmt = select(Expense).options(
        selectinload(Expense.upload_images),
        selectinload(Expense.user),
    ).where(Expense.id == expense_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 更新
async def update_expense(
        update_data: dict,
        db: AsyncSession,
):
    # 先看expenseId是否存在。
    expense = await get_expense_by_id(int(update_data['id']), db)
    if not expense:
        return None
    # 3. 更新对象的属性
    # 遍历 update_data 中的键值对，排除掉 id (通常主键不更新)
    for key, value in update_data.items():
        if key != 'id' and hasattr(expense, key):
            setattr(expense, key, value)
    await db.commit()
    await db.refresh(expense)
    return expense


# 删除
async def delete_expense(
        expense_id: int,
        db: AsyncSession,
):
    stmt = delete(Expense).where(Expense.id == expense_id)
    await db.execute(stmt)
    await db.commit()
    return True


# 获取总数
async def get_total_list(db: AsyncSession,
                         user_id: int):
    """
    获取某用户的Expense总数
    :param db:
    :param user_id:
    :return:
    """
    return await sql.get_total_list(db, user_id, Expense)
