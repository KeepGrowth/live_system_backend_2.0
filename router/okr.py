from fastapi import Path
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud import okr
from schemas.okr import *
from utils.auth import get_current_user
from utils.common import convert_to_year_program_okr_options
from utils.response import Result
from crud.program import program
from utils.service_utils import update_okr_bind_data

# 创建api-router实例
router = APIRouter(
    prefix='/api/okr',
    tags=['okr'],
)


# 新增
@router.post('/add')
async def add_okr(
        add_okr_info: OkrAddRequest,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    if add_okr_info.program_id:
        program_info = await program.get_program_by_id(add_okr_info.program_id, db)
        add_okr_info.goal_id = program_info.goal_id
    add_okr_info.user_id = current_user_id
    result = await okr.add_okr(add_okr_info.model_dump(exclude_none=True, exclude_unset=True), db)
    return Result.success(msg='新增OKR成功', data=result.id)


# 条件查询
@router.get('/list')
async def get_okr_list(
        okr_query_params: OkrQueryParams = Query(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    okr_query_params.user_id = current_user_id
    total, result = await okr.query_okr_list(db, query_params=okr_query_params.model_dump(exclude_none=True,
                                                                                          exclude_unset=True))
    for item in result:
        item.focus_time = sum(getattr(log, 'focus_time', 0) or 0 for log in item.todo_logs)
    okr_list = [OkrDetailResponse().model_validate(r) for r in result]
    res_data = OkrDetailListResponse(okr_list=okr_list, total=total)
    return Result.success(data=res_data)


# 详情查询
@router.get('/detail/{okr_id}')
async def add_goal(
        okr_id: int = Path(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    result = await okr.get_okr_by_id(db, okr_id)
    if not result:
        return Result.error(msg='OKR不存在', code=404)
    if result.user_id != current_user_id:
        return Result.error(msg='无权限查看该OKR', code=403)
    goal_info = OkrDetailResponse.model_validate(result)
    return Result.success(data=goal_info)


# 根据项目id查询okr
@router.get('/list-by-program-id/{program_id}')
async def get_okr_list_by_program_id(
        program_id: int = Path(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    result = await okr.get_okr_list_by_program_id(db, program_id)
    okr_list = [OkrDetailResponse().model_validate(r) for r in result]
    return Result.success(data=okr_list)


@router.put('/update')
async def update_okr(
        update_data: OkrUpdateRequest,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    if update_data.user_id != current_user_id:
        return Result.error(msg='无权限更新该OKR', code=403)
    if update_data.program_id:
        program_info = await program.get_program_by_id(update_data.program_id, db)
        update_data.program_id = program_info.id
        update_data.goal_id = program_info.goal_id
    result = await okr.update_okr(update_data.model_dump(exclude_none=True, exclude_unset=True), db)
    if not result:
        return Result.error(msg='更新OKR失败', code=403)

    # 更新待办、待办日志、图片绑定的OKR
    await update_okr_bind_data(db, result)
    updated_okr = OkrItemResponse().model_validate(result)
    return Result.success(data=updated_okr)


@router.delete('/delete')
async def delete_okr(
        okr_id: int = Query(..., description="OKR id", alias="okrId"),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    target_okr = await okr.get_okr_by_id(db, okr_id)
    if target_okr.user_id != current_user_id:
        return Result.error(msg='无权限删除该OKR', code=403)
    result = await okr.delete_okr(okr_id, db)
    if not result:
        return Result.error(msg='删除OKR失败', code=404)
    return Result.success(msg='删除OKR成功')


@router.get('/multi-options')
async def get_okr_multi_options(
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """
    获取OKR的选项列表
    :param db:
    :param current_user_id:
    :return:
    """
    result = await okr.query_okr_cascade_list(db, current_user_id)
    result = convert_to_year_program_okr_options(result)
    return Result.success(data=result)
