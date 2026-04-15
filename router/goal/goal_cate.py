from fastapi import HTTPException, Path
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud.goal import goal_cate
from schemas.goal.goal_cate import *
from utils.auth import get_current_user
from utils.response import Result

# 创建api-router实例
router = APIRouter(
    prefix='/api/goal/cate',
    tags=['goal_category'],
)


@router.post('/add')
async def add_goal_category(
        goal_cate_data: GoalCategoryAddRequest,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    goal_cate_data.user_id = current_user_id
    result = await goal_cate.add_goal_category(db=db,
                                               goal_category_data=goal_cate_data.model_dump(exclude_none=True,
                                                                                            exclude_unset=True))
    new_goal_cate = GoalCategoryDetailResponse.model_validate(result)
    return Result.success(data=new_goal_cate)


@router.get('/list')
async def get_goal_cate_list(
        goal_cate_query_params: GoalCategoryQueryParams,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """
    条件分页查询某用户的目标数据
    :param goal_cate_query_params:
    :param db:
    :param current_user_id:
    :return:
    """
    goal_cate_query_params.user_id = current_user_id
    total, goal_cate_list = await goal_cate.query_goal_category_list(db,
                                                                     goal_cate_query_params.model_dump(
                                                                         exclude_none=True,
                                                                         exclude_unset=True))
    goal_cate_list = [GoalCategoryDetailResponse().model_validate(r) for r in goal_cate_list]
    res_data = GoalCategoryListResponse(goal_cate_list=goal_cate_list, total=total,
                                        has_more=total > len(goal_cate_list))
    return Result.success(data=res_data)


@router.delete('/delete/{goal_cate_id}')
async def delete_goal_cate(
        goal_cate_id: int = Path(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    result = await goal_cate.delete_goal_category(db=db, goal_category_id=goal_cate_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="目标分类不存在")
    return Result.success()


@router.put('/update')
async def update_goal_cate(
        goal_cate_data: GoalCategoryUpdateRequest,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    goal_cate_data.user_id = current_user_id
    result = await goal_cate.update_goal_category(db=db, goal_category_data=goal_cate_data.model_dump(exclude_none=True,
                                                                                                      exclude_unset=True))
    updated_goal_cate = GoalCategoryDetailResponse.model_validate(result)
    return Result.success(data=updated_goal_cate)
