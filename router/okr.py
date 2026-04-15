from fastapi import HTTPException
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud import okr
from models.users import User
from schemas.okr import *
from utils.auth import get_current_user

# 创建api-router实例
router = APIRouter(
    prefix='/api/okr',
    tags=['okr'],
)


@router.post('/add')
async def add_okr(
        add_data: OkrAddRequest,
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    print(add_data.model_dump())
    result = await okr.add_okr(add_data.model_dump(exclude_none=True, exclude_unset=True), db, current_user.id)
    new_okr = OkrItemResponse().model_validate(result)
    return success_response(message='新增OKR成功', data=new_okr)


@router.get('/list')
async def get_okr_list(
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, ge=1, description="每页数量", alias="pageSize"),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    total, result = await okr.get_okr_list(db, current_user.id, page, page_size)
    okr_list = [OkrItemResponse().model_validate(r) for r in result]
    res_data = OkrListResponse(okr_list=okr_list, total=total, has_more=total > len(okr_list))
    return success_response(message='获取OKR列表成功', data=res_data)


@router.put('/update')
async def update_okr(
        update_data: OkrUpdateRequest,
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await okr.update_okr(update_data.model_dump(exclude_none=True, exclude_unset=True), db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未找到该OKR')
    updated_okr = OkrItemResponse().model_validate(result)
    return success_response(message='更新OKR成功', data=updated_okr)


@router.delete('/delete')
async def delete_okr(
        okr_id: int = Query(..., description="OKR id", alias="okrId"),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await okr.delete_okr(okr_id, db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未找到该OKR')
    return success_response(message='删除OKR成功')
