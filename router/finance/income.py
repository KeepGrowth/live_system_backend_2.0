from fastapi import HTTPException, Body, Path
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud.finance import income
from crud.okr import get_okr_by_id
from schemas.finance.income import *
from utils.auth import get_current_user
from utils.response import Result

router = APIRouter(
    prefix='/api/income',
    tags=['income'],
)


@router.post('/add')
async def add_income(
        add_data: IncomeAddRequest,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    if add_data.okr_id:
        okr = await get_okr_by_id(db, add_data.okr_id)
        add_data.program_id = okr.program_id
        add_data.goal_id = okr.goal_id
    result = await income.add_income(add_data.model_dump(exclude_none=True, exclude_unset=True), db, current_user_id)
    return Result.success(msg='新增Income成功', data=result.id)


# 获取income详情
@router.get('/detail/{income_id}')
async def get_income_detail(
        income_id: int = Path(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """

    :param income_id:
    :param db:
    :param current_user_id:
    :return:
    """
    result = await income.get_income_by_id(income_id, db)
    if not result:
        return Result.error(msg='未找到该Income', code=404)
    if result.user_id != current_user_id:
        return Result.error(msg='无此权限', code=403)
    return Result.success(data=IncomeItemResponse().model_validate(result))


# 条件查询income列表
@router.get('/list')
async def get_income_list(
        filter_data: IncomeQueryParams = Query(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    filter_data.user_id = current_user_id
    total, result = await income.query_income_list(db=db,
                                                   query_params=filter_data.model_dump(exclude_none=True,
                                                                                       exclude_unset=True))
    income_list = [IncomeJoinItemResponse().model_validate(r) for r in result]
    res_data = IncomeJoinListResponse(income_list=income_list, total=total)
    return Result.success(data=res_data)


@router.put('/update')
async def update_income(
        update_data: IncomeUpdateRequest,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    update_data.user_id = current_user_id
    if update_data.okr_id:
        okr = await get_okr_by_id(db, update_data.okr_id)
        update_data.program_id = okr.program_id
        update_data.goal_id = okr.goal_id
    result = await income.update_income(update_data.model_dump(exclude_none=True, exclude_unset=True), db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未找到该Income')
    updated_income = IncomeItemResponse().model_validate(result)
    return Result.success(data=updated_income)


@router.delete('/{income_id}')
async def delete_income(
        income_id: int = Path(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    target_income = await income.get_income_by_id(income_id, db)
    if target_income.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='无权限删除该Income')
    result = await income.delete_income(income_id, db)
    return Result.success(data=result)
