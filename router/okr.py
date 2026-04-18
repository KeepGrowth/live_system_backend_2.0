from fastapi import HTTPException
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud import okr
from models.users import User
from schemas.okr import *
from utils.auth import get_current_user
from utils.common import convert_to_year_okr_options
from utils.response import Result

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
    result = await okr.add_okr(add_okr_info.model_dump(exclude_none=True, exclude_unset=True), db, current_user_id)
    new_okr = OkrItemResponse().model_validate(result)
    return Result.success(msg='新增OKR成功', data=new_okr)


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
    okr_list = [OkrItemResponse().model_validate(r) for r in result]
    res_data = OkrListResponse(okr_list=okr_list, total=total, has_more=total > len(okr_list))
    return Result.success(data=res_data)


@router.put('/update')
async def update_okr(
        update_data: OkrUpdateRequest,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    if update_data.user_id != current_user_id:
        return Result.error(msg='无权限更新该OKR', code=403)
    print('11111',update_data)
    result = await okr.update_okr(update_data.model_dump(exclude_none=True, exclude_unset=True), db)
    if not result:
        return Result.error(msg='更新OKR失败', code=403)
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
    total, result = await okr.query_okr_list(db, query_params={"user_id": current_user_id})
    okr_list = [r.__dict__ for r in result]
    result = convert_to_year_okr_options(okr_list)
    return Result.success(data=result)
