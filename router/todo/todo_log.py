from fastapi import HTTPException, Body, Path
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud.todo import todo_log
from models.users import User
from schemas.todo.todo_log import *
from utils.auth import get_current_user
from utils.response import Result

router = APIRouter(
    prefix='/api/todo_log',
    tags=['todo_log'],
)


# 新增
@router.post('/add')
async def add_todo_log(
        todo_log_info: TodoLogAddRequest,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    todo_log_info.user_id = current_user_id
    result = await todo_log.add_todo_log(todo_log_info.model_dump(exclude_none=True, exclude_unset=True), db,
                                         current_user_id)
    new_todo_log = TodoLogItemResponse().model_validate(result)
    return Result.success(msg='新增TodoLog成功', data=new_todo_log)


# 条件查询列表
@router.get('/list')
async def get_todo_log_list(
        filter_data: TodoLogQueryRequest = Query(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    filter_data.user_id = current_user_id
    total, result = await todo_log.query_todo_log_list(db=db,
                                                       filter_data=filter_data.model_dump(exclude_none=True,
                                                                                          exclude_unset=True))
    todo_log_list = [TodoLogItemResponse().model_validate(r) for r in result]
    res_data = TodoLogListResponse(todo_log_list=todo_log_list, total=total)
    return Result.success(data=res_data)


# 删除
@router.delete('/delete/{todo_log_id}')
async def delete_todo_log(
        todo_log_id: int = Path(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    result = await todo_log.delete_todo_log(todo_log_id, db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未找到该TodoLog')
    return Result.success()


# 更新
@router.put('/update')
async def update_todo_log(
        update_log_info: TodoLogUpdateRequest,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    # 校验权限
    if update_log_info.user_id != current_user_id:
        return Result.error(msg="无权限更新该TodoLog", code=403)
    update_log_info.user_id = current_user_id
    result = await todo_log.update_todo_log(update_log_info.model_dump(exclude_none=True, exclude_unset=True), db)
    updated_todo_log = TodoLogItemResponse().model_validate(result)
    return Result.success(data=updated_todo_log)
