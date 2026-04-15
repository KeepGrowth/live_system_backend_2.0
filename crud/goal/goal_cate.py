import datetime
from fastapi import HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from models.goal.goal import GoalCategory
from utils import sql


# 新增
async def add_goal_category(
        goal_category_data: dict,
        db: AsyncSession,
):
    new_goal_category = GoalCategory(**goal_category_data)
    db.add(new_goal_category)
    await db.commit()
    await db.refresh(new_goal_category)
    return new_goal_category


# 删除
async def delete_goal_category(
        goal_category_id: int,
        db: AsyncSession,
):
    rowcount = await sql.delete_by_id(db, GoalCategory, goal_category_id)
    return rowcount


# 获取列表
async def get_goal_category_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10,
):
    total, goal_category_list = await sql.get_list_by_user_id(db, GoalCategory, user_id, page, page_size)
    return total, goal_category_list


# 条件分页查询列表
async def query_goal_category_list(
        db: AsyncSession,
        query_params: dict,
):
    return await sql.common_query_list(db, query_params, GoalCategory)


# 更新
async def update_goal_category(
        goal_category_data: dict,
        db: AsyncSession,
):
    goal_category = await sql.get_by_id(db, GoalCategory, goal_category_data.get('id'))
    if not goal_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="目标分类不存在")
    return await sql.update_by_id(db, GoalCategory, goal_category_data.get('id'), goal_category_data)
