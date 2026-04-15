import datetime
from fastapi import HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from models.goal.goal import Goal
from utils import sql


# 新增
async def add_goal(
        goal_data: dict,
        db: AsyncSession,
        user_id: int,
):
    new_goal = Goal(**goal_data, user_id=user_id)
    db.add(new_goal)
    await db.commit()
    await db.refresh(new_goal)
    return new_goal


# 获取列表
async def get_goal_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10,
):
    total, goal_list = await sql.get_list_by_user_id(db, Goal, user_id, page, page_size)
    return total, goal_list


# 更新
async def update_goal(
        goal_data: dict,
        db: AsyncSession,
        user_id: int,
):
    goal = await sql.get_by_id(db, Goal, goal_data.get('id'))
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="目标不存在")

    if goal.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权限更新该目标")

    updated_goal = await sql.update_by_id(db, Goal, goal_data.get('id'), goal_data)
    return updated_goal


# 删除
async def delete_goal(
        goal_id: int,
        db: AsyncSession,
):
    rowcount = await sql.delete_by_id(db, Goal, goal_id)
    return rowcount
