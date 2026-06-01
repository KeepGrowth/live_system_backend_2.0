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
        selectinload(Todo.okr),
        selectinload(Todo.program),
        selectinload(Todo.goal),
        selectinload(Todo.todo_logs).options(
            selectinload(TodoLog.upload_images)
        ),
        selectinload(Todo.upload_images)
    )
    # 比较时间
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


# 根据okrid查询todo
async def get_todo_by_okr_id(
        okr_id: int,
        db: AsyncSession,
):
    """
    根据id查询todo
    """
    stmt = select(Todo).where(Todo.okr_id == okr_id)
    result = await db.execute(stmt)
    return result.scalars().all()



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
