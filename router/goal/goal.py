from fastapi import HTTPException
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud.goal import goal
from models.users import User
from schemas.goal.goal import GoalAddRequest, GoalDetailResponse, GoalListResponse, GoalUpdateRequest
from utils.auth import get_current_user

# 创建api-router实例
router = APIRouter(
    prefix='/api/goal',
    tags=['goal'],
)


@router.post('/add')
async def add_goal(
        goal_data: GoalAddRequest,
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await goal.add_goal(db=db, user_id=current_user.id,
                                 goal_data=goal_data.model_dump(exclude_none=True, exclude_unset=True))
    new_goal = GoalDetailResponse.model_validate(result)
    return success_response(message="新增目标成功", data=new_goal)


@router.get('/list')
async def get_goal_list(
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, ge=1, description="每页数量", alias="pageSize"),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    total, result = await goal.get_goal_list(db=db, user_id=current_user.id, page=page, page_size=page_size)
    goal_list = [GoalDetailResponse.model_validate(item.__dict__) for item in result]
    goal_list = GoalListResponse(total=total, goal_list=goal_list, has_more=total > page * page_size)
    return success_response(message="获取目标列表成功", data=goal_list)


# 删除
@router.delete('/delete')
async def delete_goal(
        goal_id: int = Query(..., description="目标id", alias="goalId"),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await goal.delete_goal(db=db, goal_id=goal_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="目标不存在")
    return success_response(message="删除目标成功")


# 更新
@router.put('/update')
async def update_goal(
        goal_data: GoalUpdateRequest,
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await goal.update_goal(db=db, goal_data=goal_data.model_dump(exclude_none=True, exclude_unset=True),
                                    user_id=current_user.id)
    updated_goal = GoalDetailResponse.model_validate(result)
    return success_response(message="更新目标成功", data=updated_goal)
