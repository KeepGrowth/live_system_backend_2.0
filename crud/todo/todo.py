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
        filter_data: dict,
):
    # 1. 初始化总数查询和列表查询的基础语句（都限定当前用户）
    total_stmt = select(func.count(Todo.id))
    list_stmt = select(Todo)

    # 2. 定义允许的筛选字段白名单，防止非法字段注入
    allow_filter_keys = [
        'status',
        'goal_id',
        'program_id',
        'okr_id',
        'start_date',
        'end_date',
        'page',
        'page_size',
        'user_id'
    ]
    # 3. 提取并处理分页参数
    # 获取页码，默认为 1
    page = filter_data.get('page', 1)
    try:
        page = int(page)
        page = max(1, page)  # 保证页码至少为 1
    except (ValueError, TypeError):
        page = 1

    # 获取每页数量，默认为 10
    page_size = filter_data.get('page_size', 10)
    try:
        page_size = int(page_size)
        # 限制最大每页数量，防止恶意请求过大导致数据库压力
        page_size = min(page_size, 100)
    except (ValueError, TypeError):
        page_size = 10

    # 计算偏移量 (offset = (页码 - 1) * 每页数量)
    offset = (page - 1) * page_size

    # 去除page和page_size参数
    filter_data.pop('page', None)
    filter_data.pop('page_size', None)

    # 提取筛选条件
    filter_conditions = build_filter_conditions(Todo, allow_filter_keys, filter_data)

    # 4. 如果有筛选条件，添加到查询语句中
    if filter_conditions:
        total_stmt = total_stmt.where(and_(*filter_conditions))
        list_stmt = list_stmt.where(and_(*filter_conditions))

    # 5. 分页
    list_stmt = list_stmt.offset(offset).limit(page_size)

    # 6. 执行数据库查询（异步执行）
    # 获取总数
    total_result = await db.execute(total_stmt)
    total = total_result.scalar() or 0  # 提取总数的标量值

    # 获取列表数据
    list_result = await db.execute(list_stmt)
    todo_list = list_result.scalars().all() or []  # 提取Todo对象列表
    # 7. 返回结果（总数+列表，方便前端做分页展示）
    return total, todo_list


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
    stmt = select(Todo).where(Todo.id == todo_id)
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
