import datetime
from fastapi import HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, and_
from models.todo.todo_log import TodoLog
from schemas.todo.todo_log import *
from utils import sql


# 提取条件查询
def build_filter_conditions(
        model,  # 传入的模型类（比如Todo、Task等）
        allow_filter_keys: list,  # 允许的筛选字段白名单列表
        filter_data: dict,  # 前端传入的筛选条件字典
        date_field_map: dict = None  # 日期字段映射（可选，指定哪些字段对应模型的哪个日期字段）
):
    """
    通用筛选条件拼接方法
    :param model: 数据模型类（如Todo）
    :param allow_filter_keys: 允许的筛选字段列表，如['status', 'start_date', 'end_date']
    :param filter_data: 筛选条件字典，如{"status": "done", "start_date": "2026-02-01"}
    :param date_field_map: 日期字段映射，默认{"start_date": "deadline", "end_date": "deadline"}，可自定义
    :return: 拼接好的筛选条件列表
    """
    # 默认日期字段映射（如果前端传start_date/end_date，对应模型的deadline字段）
    if date_field_map is None:
        date_field_map = {
            "start_date": "create_time",
            "end_date": "create_time"
        }

    filter_conditions = []
    # 遍历筛选条件，只处理白名单内的字段
    for key in filter_data.keys():
        if key not in allow_filter_keys:
            continue

        value = filter_data[key]
        # 跳过空值（None/空字符串）
        if value is None or value == "":
            continue

        # 处理日期字段（start_date/end_date）
        if key in date_field_map:
            model_field = getattr(model, date_field_map[key])
            if key == "start_date":
                filter_conditions.append(model_field >= value)
            elif key == "end_date":
                filter_conditions.append(model_field <= value)
        # 处理普通字段（等值匹配）
        else:
            model_field = getattr(model, key)
            filter_conditions.append(model_field == value)
    print(filter_conditions)

    return filter_conditions


# 新增
async def add_todo_log(add_data: dict, db: AsyncSession, user_id: int):
    return await sql.add(db=db, model=TodoLog, user_id=user_id, add_data=add_data)


# 条件查询列表
async def query_todo_log_list(db: AsyncSession, user_id: int, filter_data: dict):
    allow_filter_keys = ['user_id', 'todo_id', 'goal_id', 'program_id', 'okr_id', 'title', 'score', 'log_desc',
                         'attachment_path', 'start_date', 'end_date']
    conditions = build_filter_conditions(TodoLog, allow_filter_keys, filter_data)
    total_stmt = select(func.count(TodoLog.id)).where(TodoLog.user_id == user_id)
    list_stmt = select(TodoLog).where(TodoLog.user_id == user_id)
    if conditions:
        total_stmt = total_stmt.where(and_(*conditions))
        list_stmt = list_stmt.where(and_(*conditions))
    total = await db.execute(total_stmt)
    total = total.scalar_one()
    list_result = await db.execute(list_stmt)
    todo_log_list = list_result.scalars().all()
    return total, todo_log_list


# 删除
async def delete_todo_log(todo_log_id: int, db: AsyncSession):
    return await sql.delete_by_id(db=db, model=TodoLog, id=todo_log_id)


# 更新
async def update_todo_log(update_data: dict, db: AsyncSession):
    return await sql.update_by_id(db=db, model=TodoLog, update_data=update_data, item_id=update_data['id'])
