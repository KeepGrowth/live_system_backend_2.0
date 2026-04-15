import datetime
from fastapi import HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from models.project.project import Project
from schemas.project.project import ProjectAddRequest, ProjectUpdateRequest
from utils import sql


# 新增单子
async def add_project(
        project_data: dict,
        db: AsyncSession,
        user_id: int,
):
    new_project = Project(**project_data, user_id=user_id)
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project


# 获取单子列表
async def get_project_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10,
):
    total, result = await sql.get_list_by_user_id(db, Project, user_id, page, page_size)
    return total, result


# 根据id获取单子详情
async def get_project_by_id(
        db: AsyncSession,
        project_id: int,
):
    stmt = select(Project).where(Project.id == project_id)
    project = await db.execute(stmt)
    return project.scalar_one_or_none()


# 更新单子详情
async def update_project(
        db: AsyncSession,
        project_id: int,
        update_data: ProjectUpdateRequest,
):
    project = await get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="单子不存在")
    # 生成更新字典：过滤掉None值，只更新传了值的字段
    update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
    # 3. 遍历更新字典，给project实例赋值
    for key, value in update_dict.items():
        # 安全检查：确保要更新的字段是project实例的属性
        if hasattr(project, key):
            setattr(project, key, value)
    project.update_time = datetime.datetime.now()
    await db.commit()
    await db.refresh(project)
    return project


# 删除单子
async def delete_project(
        db: AsyncSession,
        project_id: int,
):
    project = await get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="单子不存在")
    stmt = delete(Project).where(Project.id == project_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount
