"""
IT兼职项目表接口。
"""
from fastapi import HTTPException
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud.project import project
from models.users import User
from schemas.project.project import ProjectAddRequest, ProjectDetailResponse, ProjectListResponse, ProjectUpdateRequest
from utils.auth import get_current_user

# 创建api-router实例
router = APIRouter(
    prefix='/api/project',
    tags=['project'],
)


# 新增单子
@router.post('/add')
async def add_project(
        project_data: ProjectAddRequest,
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await project.add_project(db=db, user_id=current_user.id,
                                       project_data=project_data.model_dump(exclude_unset=True,
                                                                            exclude_none=True))
    res_data = ProjectDetailResponse().model_validate(result.__dict__)
    return success_response(message=f"用户{current_user.username}新增项目成功", data=res_data)


# 获取单子列表
@router.get('/list')
async def get_project_list(
        page: int = Query(1, description="页码"),
        page_size: int = Query(10, description="每页数量", alias="pageSize"),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user),
):
    total, result = await project.get_project_list(db=db, user_id=current_user.id, page=page, page_size=page_size)
    has_more = total > page * page_size
    project_list = [ProjectDetailResponse().model_validate(item.__dict__) for item in result]

    res_data = ProjectListResponse(project_list=project_list, total=total, has_more=has_more)
    return success_response(message="获取项目列表成功", data=res_data)


# 获取单子详情
@router.get('/detail')
async def get_project_detail(
        project_id: int = Query(..., description="单子id", alias="projectId"),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user),
):
    result = await project.get_project_by_id(db=db, project_id=project_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="单子不存在")
    res_data = ProjectDetailResponse().model_validate(result)
    return success_response(message=f"用户{current_user.username}获取单子详情成功", data=res_data)


# 更新单子详情
@router.put('/update')
async def update_project(
        update_data: ProjectUpdateRequest,
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user),
):
    updated_project = await project.update_project(db=db, project_id=update_data.id, update_data=update_data)
    return success_response(message=f"用户{current_user.username}更新单子成功", data=updated_project)


# 删除单子
@router.delete('/delete')
async def delete_project(
        project_id: int = Query(..., description="单子id", alias="projectId"),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user),
):
    result = await project.delete_project(db=db, project_id=project_id)
    return success_response(message=f"用户{current_user.username}删除{result}条单子成功", data=result)
