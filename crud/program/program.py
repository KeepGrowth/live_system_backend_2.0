import datetime
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, inspect, and_, cast, Date

from models.okr import Okr
from models.program import Program, ProgramLog
from models.program import Program
from utils import security, sql
from utils.sql import build_filter_conditions


# 新增项目
async def add_program(
        program_info: dict,
        db: AsyncSession,
):
    new_program = Program(**program_info)
    db.add(new_program)
    await db.commit()
    await db.refresh(new_program)
    return new_program


# 分页条件获取项目列表
async def get_program_list(
        db: AsyncSession,
        query_params: dict = None,
):
    """
    分页-条件查询项目列表
    :param db:
    :param query_params:
    :return:
    """
    list_stmt = select(Program).options(
        selectinload(Program.program_log),
        selectinload(Program.user),
        selectinload(Program.goal),
        selectinload(Program.okrs),
        selectinload(Program.todo_logs),
        selectinload(Program.upload_images)
    )
    # 1. 初始化总数查询和列表查询的基础语句（都限定当前用户）
    total_stmt = select(func.count(Program.id))
    if query_params.get('keyword', None):
        list_stmt = list_stmt.where(Program.program_name.like(f"%{query_params.get('keyword')}%"))
        total_stmt = total_stmt.where(Program.program_name.like(f"%{query_params.get('keyword')}%"))
        query_params.pop('keyword')

    if query_params.get('start_year', None):
        start_date = datetime.date(query_params.get('start_year'), 1, 1)
        total_stmt = total_stmt.where(Program.estimate_start_time >= start_date)
        list_stmt = list_stmt.where(Program.estimate_start_time >= start_date)
        query_params.pop('start_year')
    if query_params.get('end_year', None):
        end_date = datetime.date(query_params.get('end_year'), 12, 31)
        total_stmt = total_stmt.where(cast(Program.estimate_start_time, Date) <= end_date)
        list_stmt = list_stmt.where(Program.estimate_start_time <= end_date)
        query_params.pop('end_year')

    return await sql.common_query_list(db, query_params, total_stmt, list_stmt, Program)


# 获取项目详情
async def get_program_by_id(
        program_id: int,
        db: AsyncSession,
):
    query = select(Program).options(
        selectinload(Program.upload_images),
        selectinload(Program.user),
        selectinload(Program.okrs),
        selectinload(Program.goal),
        selectinload(Program.todo_logs),
        selectinload(Program.program_log),
    ).where(Program.id == program_id)
    result = await db.execute(query)
    program_detail = result.scalar_one_or_none()
    return program_detail


# 更新项目信息
async def update_program(
        update_data: dict,
        db: AsyncSession,
):
    # 查找项目是否存在
    query = select(Program).where(Program.id == update_data.get('id'))
    result = await db.execute(query)
    db_program = result.scalar_one_or_none()
    if not db_program:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="项目不存在")
    return await sql.update_by_id(db, Program, update_data['id'], update_data)


# 删除
async def delete_program(
        program_id: int,
        db: AsyncSession,
):
    query = select(Program).where(Program.id == program_id)
    result = await db.execute(query)
    db_program = result.scalar_one_or_none()
    if not db_program:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="项目不存在")
    return await sql.delete_by_id(db, Program, program_id)


# 获取综述
async def get_total_list(db: AsyncSession,
                         user_id: int):
    """
    获取某用户的项目总数
    :param db:
    :param user_id:
    :return:
    """
    return await sql.get_total_list(db, user_id, Program)
