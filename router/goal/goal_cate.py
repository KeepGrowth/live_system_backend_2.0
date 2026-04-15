from fastapi import HTTPException
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud.goal import goal_cate
from models.users import User
from schemas.goal.goal_cate import *
from utils.auth import get_current_user

# 创建api-router实例
router = APIRouter(
    prefix='/api/goal/cate',
    tags=['goal_category'],
)


@router.post('/add')
async def add_goal_category(
        goal_cate_data: GoalCategoryAddRequest,
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await goal_cate.add_goal_category(db=db, user_id=current_user.id,
                                               goal_category_data=goal_cate_data.model_dump(exclude_none=True,
                                                                                            exclude_unset=True))
    new_goal_cate = GoalCategoryDetailResponse.model_validate(result)
    return success_response(message="新增目标分类成功", data=new_goal_cate)


@router.get('/list')
async def get_goal_cate_list(
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, ge=1, description="每页数量", alias="pageSize"),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    total, result = await goal_cate.get_goal_category_list(db=db, user_id=current_user.id, page=page,
                                                           page_size=page_size)
    goal_cate_list = [GoalCategoryDetailResponse.model_validate(item) for item in result]
    print(goal_cate_list)
    res_data = GoalCategoryListResponse(total=total, goal_category_list=goal_cate_list,
                                        has_more=total > page * page_size)
    print(res_data)
    return success_response(message="获取目标分类列表成功", data=res_data)


@router.delete('/delete')
async def delete_goal_cate(
        goal_cate_id: int = Query(..., description="目标分类id", alias="goalCategoryId"),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await goal_cate.delete_goal_category(db=db, goal_category_id=goal_cate_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="目标分类不存在")
    return success_response(message="删除目标分类成功")


@router.put('/update')
async def update_goal_cate(
        goal_cate_data: GoalCategoryUpdateRequest,
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await goal_cate.update_goal_category(db=db, goal_category_data=goal_cate_data.model_dump(exclude_none=True,
                                                                                                      exclude_unset=True))
    updated_goal_cate = GoalCategoryDetailResponse.model_validate(result)
    return success_response(message="更新目标分类成功", data=updated_goal_cate)
