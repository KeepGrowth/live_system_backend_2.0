import datetime
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from models.goal.goal import Goal
from models.okr import Okr
from models.program import Program
from models.todo.todo import Todo
from utils import sql


# 新增
async def add_goal(
        goal_data: dict,
        db: AsyncSession,
):
    new_goal = Goal(**goal_data)
    db.add(new_goal)
    await db.commit()
    await db.refresh(new_goal)
    return new_goal


# 根据id获取目标信息
async def get_goal_by_id(
        goal_id: int,
        db: AsyncSession,
):
    """
    根据id获取目标
    :param goal_id:
    :param db:
    :return:
    """
    return await sql.get_by_id(db, Goal, goal_id)


# 获取列表
async def query_goal_list(
        db: AsyncSession,
        query_params: dict = None,
):
    list_stmt = select(Goal).options(
        selectinload(Goal.programs).selectinload(Program.program_log),
        selectinload(Goal.programs).selectinload(Program.upload_images),
        selectinload(Goal.programs).selectinload(Program.okrs).
        selectinload(Okr.todos).selectinload(Todo.todo_logs),
        selectinload(Goal.upload_images),
    )
    # 1. 初始化总数查询和列表查询的基础语句（都限定当前用户）
    total_stmt = select(func.count(Goal.id))
    return await sql.common_query_list(db, query_params, total_stmt, list_stmt, Goal)


# 更新
async def update_goal(
        goal_data: dict,
        db: AsyncSession,
):
    updated_goal = await sql.update_by_id(db, Goal, goal_data.get('id'), goal_data)
    return updated_goal


# 删除
async def delete_goal(
        goal_id: int,
        db: AsyncSession,
):
    rowcount = await sql.delete_by_id(db, Goal, goal_id)
    return rowcount
