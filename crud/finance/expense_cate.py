import datetime
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, and_

from models.finance.expense import Expense, ExpenseCate, ExpenseSecondCate
from utils import sql


# 获取列表
async def query_first_cate_list(
        db: AsyncSession,
        user_id: int,
):
    total_stmt = select(func.count(ExpenseCate.id)).where(ExpenseCate.user_id == user_id)
    stmt = select(ExpenseCate).where(ExpenseCate.user_id == user_id)
    result = await db.execute(stmt)
    total = await db.execute(total_stmt)
    return total.scalar_one(), result.scalars().all()
