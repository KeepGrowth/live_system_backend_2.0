from fastapi import HTTPException, Path
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud.goal import goal
from models.users import User
from schemas.goal.goal import GoalAddRequest, GoalDetailResponse, GoalListResponse, GoalUpdateRequest, GoalQueryParams
from utils.auth import get_current_user
from utils.common import convert_to_year_goal_options
from utils.response import Result

# 创建api-router实例
router = APIRouter(
    prefix='/api/goal',
    tags=['goal'],
)


@router.post('/add')
async def add_goal(
        goal_data: GoalAddRequest,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    goal_data.user_id = current_user_id
    result = await goal.add_goal(db=db,
                                 goal_data=goal_data.model_dump(exclude_none=True, exclude_unset=True))
    new_goal = GoalDetailResponse.model_validate(result)
    return Result.success(data=new_goal)


@router.get('/list')
async def get_goal_list(
        goal_query_params: GoalQueryParams = Query(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """
    条件分页查询目标数据列表
    :param goal_query_params:条件查询参数
    :param db:
    :param current_user_id:
    :return:
    """
    goal_query_params.user_id = current_user_id
    total, goal_list = await goal.query_goal_list(db,
                                                  goal_query_params.model_dump(exclude_none=True, exclude_unset=True))
    goal_list = [GoalDetailResponse().model_validate(r) for r in goal_list]
    res_data = GoalListResponse(total=total, goal_list=goal_list, has_more=total > len(goal_list))
    return Result.success(data=res_data)


# 删除
@router.delete('/delete/{goal_id}')
async def delete_goal(
        goal_id: int = Path(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    target_goal = await goal.get_goal_by_id(goal_id, db)
    if target_goal.user_id != current_user_id:
        return Result.error(msg='无权限删除该目标', code=403)
    result = await goal.delete_goal(goal_id, db)
    if not result:
        return Result.error(msg='删除目标失败', code=404)
    return Result.success(msg="删除目标成功")


# 更新
@router.put('/update')
async def update_goal(
        goal_data: GoalUpdateRequest,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    target_goal = await goal.get_goal_by_id(goal_data.id, db)
    if target_goal.user_id != current_user_id:
        return Result.error(msg='无权限更新该目标', code=403)
    # 执行更新
    goal_data.user_id = current_user_id
    result = await goal.update_goal(db=db,
                                    goal_data=goal_data.model_dump(exclude_none=True, exclude_unset=True)
                                    )
    updated_goal = GoalDetailResponse.model_validate(result)
    return Result.success(data=updated_goal)


# 获取目标级联选项
@router.get('/multi-options')
async def get_goal_multi_options(
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """
    根据用户ID，获取所有年份的所有目标，更改数据格式为级联选项格式。
    """
    total, result = await goal.query_goal_list(db, query_params={"user_id": current_user_id})
    goal_list = [GoalDetailResponse().model_validate(r) for r in result]
    result = convert_to_year_goal_options(goal_list)
    return Result.success(data=result)
