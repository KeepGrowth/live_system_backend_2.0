import datetime
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, and_
from models.todo.todo import Todo
from models.todo.todo_log import TodoLog
from schemas.todo.todo import TodoAddRequest, TodoUpdateRequest
from utils import sql


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
            "start_date": "deadline",
            "end_date": "deadline"
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

    return filter_conditions


# 新增
async def add_todo(
        add_data: dict,
        db: AsyncSession,
        user_id: int,
):
    new_todo = Todo(**add_data, user_id=user_id)
    db.add(new_todo)
    await db.commit()
    await db.refresh(new_todo)
    return new_todo


# 条件查询列表-分页
async def query_todo_list(
        db: AsyncSession,
        query_params: dict,
):
    # 1. 初始化总数查询和列表查询的基础语句（都限定当前用户）
    total_stmt = select(func.count(Todo.id))
    list_stmt = select(Todo).options(
        selectinload(Todo.user),
        selectinload(Todo.todo_logs).options(
            selectinload(TodoLog.upload_images)
        ),
        selectinload(Todo.upload_images)
    )
    # 比较年份
    if query_params.get('start_date', None):
        total_stmt = total_stmt.where(Todo.deadline >= query_params.get('start_date'))
        list_stmt = list_stmt.where(Todo.deadline >= query_params.get('start_date'))
        query_params.pop('start_date')
    if query_params.get('end_date', None):
        total_stmt = total_stmt.where(Todo.deadline <= query_params.get('end_date'))
        list_stmt = list_stmt.where(Todo.deadline <= query_params.get('end_date'))
        query_params.pop('end_date')
    return await sql.common_query_list(db, query_params, total_stmt, list_stmt, Todo)


# 根据id查询todo
async def get_todo_by_id(
        todo_id: int,
        db: AsyncSession,
):
    """
    根据id查询todo
    :param todo_id:
    :param db:
    :return:
    """
    stmt = select(Todo).options(
        selectinload(Todo.upload_images),
        selectinload(Todo.user),
    ).where(Todo.id == todo_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 更新
async def update_todo(
        update_data: dict,
        db: AsyncSession,
):
    # 先看todoId是否存在。
    todo = await get_todo_by_id(int(update_data['id']), db)
    if not todo:
        return None
    # 3. 更新对象的属性
    # 遍历 update_data 中的键值对，排除掉 id (通常主键不更新)
    for key, value in update_data.items():
        if key != 'id' and hasattr(todo, key):
            setattr(todo, key, value)
    await db.commit()
    await db.refresh(todo)
    return todo


# 删除
async def delete_todo(
        todo_id: int,
        db: AsyncSession,
):
    stmt = delete(Todo).where(Todo.id == todo_id)
    await db.execute(stmt)
    await db.commit()
    return True


# 获取综述
async def get_total_list(db: AsyncSession,
                         user_id: int):
    """
    获取某用户的Todo总数
    :param db:
    :param user_id:
    :return:
    """
    return await sql.get_total_list(db, user_id, Todo)
