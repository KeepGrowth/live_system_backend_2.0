import datetime
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, and_

from models.finance.expense import Expense, ExpenseSecondCate, ExpenseSecondCate
from utils import sql


# 获取列表
async def query_second_cate_list(
        db: AsyncSession,
        user_id: int,
        first_cate_id: int,
):
    total_stmt = select(func.count(ExpenseSecondCate.id)).where(ExpenseSecondCate.user_id == user_id).where(
        ExpenseSecondCate.first_cate_id == first_cate_id)
    stmt = select(ExpenseSecondCate).where(ExpenseSecondCate.user_id == user_id).where(
        ExpenseSecondCate.first_cate_id == first_cate_id)
    result = await db.execute(stmt)
    total = await db.execute(total_stmt)
    return total.scalar_one(), result.scalars().all()
