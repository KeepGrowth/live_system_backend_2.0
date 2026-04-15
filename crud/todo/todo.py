import datetime
from fastapi import HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, and_
from models.todo.todo import Todo
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
    print(filter_conditions)

    return filter_conditions


# 新增
async def add_todo(
        add_data: dict,
        db: AsyncSession,
        user_id: int,
):
    new_todo = await sql.add(db, Todo, user_id, add_data)
    return new_todo


# 条件查询列表
async def query_todo_list(
        db: AsyncSession,
        user_id: int,
        filter_data: dict,
):
    # 1. 初始化总数查询和列表查询的基础语句（都限定当前用户）
    total_stmt = select(func.count(Todo.id)).where(Todo.user_id == user_id)
    list_stmt = select(Todo).where(Todo.user_id == user_id)

    # 2. 定义允许的筛选字段白名单，防止非法字段注入
    allow_filter_keys = [
        'status',
        'goal_id',
        'program_id',
        'okr_id',
        'start_date',
        'end_date',
    ]

    # 提取筛选条件
    filter_conditions = build_filter_conditions(Todo, allow_filter_keys, filter_data)

    # 4. 如果有筛选条件，添加到查询语句中
    if filter_conditions:
        total_stmt = total_stmt.where(and_(*filter_conditions))
        list_stmt = list_stmt.where(and_(*filter_conditions))

    # 6. 执行数据库查询（异步执行）
    # 获取总数
    total_result = await db.execute(total_stmt)
    total = total_result.scalar()  # 提取总数的标量值

    # 获取列表数据
    list_result = await db.execute(list_stmt)
    todo_list = list_result.scalars().all()  # 提取Todo对象列表
    # 7. 返回结果（总数+列表，方便前端做分页展示）
    return total, todo_list


# 更新
async def update_todo(
        update_data: dict,
        db: AsyncSession,
):
    todo = await sql.update_by_id(db=db, model=Todo, item_id=update_data['id'], update_data=update_data)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未找到该Todo')
    return todo


# 删除
async def delete_todo(
        todo_id: int,
        db: AsyncSession,
):
    result = await sql.delete_by_id(db=db, model=Todo, id=todo_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未找到该Todo')
    return result
