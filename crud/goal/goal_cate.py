import datetime
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete

from cache.goal_cache import get_cached_categories, set_cache_categories
from config.cache_conf import set_cache
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

):
    """
    带缓存的读取目标分类列表数据方法。
    :param db:
    :param user_id:用户ID
    :return:
    """
    # 先从缓存中获取数据
    goal_cate_list = await get_cached_categories()
    if goal_cate_list:
        return goal_cate_list
    stmt = select(GoalCategory).where(GoalCategory.user_id == user_id)
    result = await db.execute(stmt)
    categories = result.scalars().all()  # ORM

    # 写入缓存
    if categories:
        categories = jsonable_encoder(categories)  # 把ORM等复杂对象转为JSON能认识的格式-例如JSON数组。
        await set_cache_categories(categories)
    # 写入缓存
    return categories


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
