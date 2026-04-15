"""
单子来源分类接口
"""
from fastapi import HTTPException
from starlette import status
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud.project import project_channel
from models.users import User
from schemas.project.project_channel import ProjectChannelDetailResponse, ProjectChannelListResponse, \
    ProjectChannelAddRequest
from utils.auth import get_current_user

# 创建api-router实例
router = APIRouter(
    prefix='/api/project/channel',
    tags=['project_channel'],
)


@router.post('/add')
async def add_project_channel(
        channel_data: ProjectChannelAddRequest,
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    print(channel_data.model_dump())
    result = await project_channel.add_project_channel(db=db, user_id=current_user.id,
                                                       channel_data=channel_data.model_dump())
    res_data = ProjectChannelDetailResponse().model_validate(result.__dict__)
    return success_response(message=f"用户{current_user.username}新增项目来源渠道成功", data=res_data)


@router.delete('/delete')
async def delete_project_channel(
        channel_id: int = Query(..., description="项目来源渠道id", alias="channelId"),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    """
    删除分类
    """
    result = await project_channel.delete_project_channel(db=db, channel_id=channel_id)
    return success_response(message=f"用户{current_user.username}删除项目来源渠道成功", data=result)


# 获取分类列表
@router.get('/list')
async def get_project_channel_list(
        page: int = Query(1, description="页码", alias="page"),
        page_size: int = Query(10, description="每页数量", alias="pageSize"),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    total, result = await project_channel.get_project_channel_list(
        db=db,
        user_id=current_user.id,
        page=page,
        page_size=page_size
    )
    has_more = total > page * page_size
    res_project_channel_list = [ProjectChannelDetailResponse().model_validate(item.__dict__) for item in
                                result]
    res_data = ProjectChannelListResponse(has_more=has_more, channel_list=res_project_channel_list, total=total)
    return success_response(message=f"用户{current_user.username}获取项目来源渠道列表成功", data=res_data)


# 更新分类
@router.put('/update')
async def update_project_channel(
        channel_id: int = Query(..., description="项目来源渠道id", alias="channelId"),
        channel_name: str = Query(..., description="项目来源渠道名称", alias="channelName"),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await project_channel.update_project_channel(
        db=db,
        channel_id=channel_id,
        channel_name=channel_name
    )
    res_data = ProjectChannelDetailResponse().model_validate(result)
    return success_response(message=f"用户{current_user.username}更新项目来源渠道成功", data=res_data)
