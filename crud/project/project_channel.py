import datetime
from fastapi import HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from models.project.project import ProjectChannel
from schemas.project.project import ProjectAddRequest, ProjectUpdateRequest
from utils import sql


# 新增分类
async def add_project_channel(
        db: AsyncSession,
        user_id: int,
        channel_data: dict,
):
    new_channel = ProjectChannel(**channel_data, user_id=user_id)
    db.add(new_channel)
    await db.commit()
    await db.refresh(new_channel)
    return new_channel


# 删除分类
async def delete_project_channel(
        db: AsyncSession,
        channel_id: int,
):
    rowcount = await sql.delete_by_id(db, ProjectChannel, channel_id)
    return rowcount


# 获取分类列表
async def get_project_channel_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10,
):
    total, project_channel_list = await sql.get_list_by_user_id(db, ProjectChannel, user_id, page, page_size)

    return total, project_channel_list


# 更新分类
async def update_project_channel(
        db: AsyncSession,
        channel_id: int,
        channel_name: str,
):
    channel = sql.get_by_id(db, ProjectChannel, channel_id)
    if not channel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="分类不存在")
    channel.channel_name = channel_name
    await db.commit()
    await db.refresh(channel)
    return channel
