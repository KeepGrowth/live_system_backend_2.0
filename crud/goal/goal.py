import datetime
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import model_validator
from sqlalchemy.orm import selectinload, joinedload
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete

from cache import goal_cache
from models.goal.goal import Goal
from models.okr import Okr
from models.program import Program
from models.todo.todo import Todo
from schemas.goal.goal import GoalJoinItemResponse
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
    stmt = ((select(Goal).options(
        selectinload(Goal.user),
        selectinload(Goal.programs).options(
            selectinload(Program.upload_images),
            selectinload(Program.program_log),
        ),
        selectinload(Goal.upload_images),
        selectinload(Goal.goal_category),
    )).where(Goal.id == goal_id))
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 获取列表
async def query_goal_list(
        db: AsyncSession,
        query_params: dict,
):
    """
    带缓存-分页-分类-查询目标列表数据。
    :param db:
    :param query_params:
    :return:
    """
    # 先从缓存读取数据
    goal_list = await goal_cache.get_cached_goals(
        page=query_params.get('page', None),
        page_size=query_params.get('page_size', None),
        first_cate_id=query_params.get('first_cate_id', None),
        user_id=query_params.get('user_id', None),
    )
    if goal_list:
        return len(goal_list), goal_list
    list_stmt = select(Goal).options(
        selectinload(Goal.user),
        selectinload(Goal.programs).options(
            selectinload(Program.upload_images),
        ),
        selectinload(Goal.upload_images),
        selectinload(Goal.todos),
        selectinload(Goal.goal_category),
    )
    # 1. 初始化总数查询和列表查询的基础语句（都限定当前用户）
    total_stmt = select(func.count(Goal.id))
    if query_params.get('keyword', None):
        list_stmt = list_stmt.where(
            Goal.goal_name.like(f'%{query_params.get("keyword")}%')
        )
        total_stmt = total_stmt.where(
            Goal.goal_name.like(f'%{query_params.get("keyword")}%')
        )
        query_params.pop('keyword')

    # 比较年份
    if query_params.get('start_year', None):
        total_stmt = total_stmt.where(Goal.start_date >= datetime.date(query_params.get('start_year'), 1, 1))
        list_stmt = list_stmt.where(Goal.start_date >= datetime.date(query_params.get('start_year'), 1, 1))
        query_params.pop('start_year')
    if query_params.get('end_year', None):
        total_stmt = total_stmt.where(Goal.start_date <= datetime.date(query_params.get('end_year'), 12, 31))
        list_stmt = list_stmt.where(Goal.start_date <= datetime.date(query_params.get('end_year'), 12, 31))
        query_params.pop('end_year')

    total, goal_list = await sql.common_query_list(db, query_params, total_stmt, list_stmt, Goal)

    # 写入缓存
    if goal_list:
        # 将数据转为pydantic类型
        goal_data = [GoalJoinItemResponse.model_validate(item).model_dump(mode="json", by_alias=False) for item in
                     goal_list]
        await goal_cache.set_cached_goals(
            page=query_params.get('page', None),
            page_size=query_params.get('page_size', None),
            first_cate_id=query_params.get('first_cate_id', None),
            user_id=query_params['user_id'],
            goal_list=goal_data,
        )
    return total, goal_list


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


# 获取总数
async def get_total_list(db: AsyncSession,
                         user_id: int):
    """
    获取某用户的目标总数
    :param db:
    :param user_id:
    :return:
    """
    stmt = (
        select(Goal)
        .where(Goal.user_id == user_id)
        .options(joinedload(Goal.goal_category))
    )

    result = await db.execute(stmt)
    return result.scalars().all()
