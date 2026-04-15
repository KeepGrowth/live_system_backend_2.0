import datetime
import uuid
from fastapi import HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.program import Program, ProgramLog
from utils import security, sql


# 新增项目
async def add_program(
        program_name: str,
        db: AsyncSession,
        user_id: int,
):
    new_program = Program(program_name=program_name, user_id=user_id)
    db.add(new_program)
    await db.commit()
    await db.refresh(new_program)
    return new_program


# 获取项目列表
async def get_program_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10,
):
    return await sql.get_list_by_user_id(db, Program, user_id, page, page_size)


# 获取项目详情
async def get_program_detail(
        program_id: int,
        db: AsyncSession,
):
    query = select(Program).where(Program.id == program_id)
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
