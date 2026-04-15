from fastapi import HTTPException, Body
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud.todo import todo_log
from models.users import User
from schemas.todo.todo_log import *
from utils.auth import get_current_user

router = APIRouter(
    prefix='/api/todo_log',
    tags=['todo_log'],
)


# 新增
@router.post('/add')
async def add_todo_log(
        add_data: TodoLogAddRequest = Body(...),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await todo_log.add_todo_log(add_data.model_dump(exclude_none=True, exclude_unset=True), db,
                                         current_user.id)
    new_todo_log = TodoLogItemResponse().model_validate(result)
    return success_response(message='新增TodoLog成功', data=new_todo_log)


# 条件查询列表
@router.get('/list')
async def get_todo_log_list(
        filter_data: TodoLogQueryRequest = Query(...),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    total, result = await todo_log.query_todo_log_list(db=db,
                                                       user_id=current_user.id,
                                                       filter_data=filter_data.model_dump(exclude_none=True,
                                                                                          exclude_unset=True))
    todo_log_list = [TodoLogItemResponse().model_validate(r) for r in result]
    res_data = TodoLogListResponse(todo_log_list=todo_log_list, total=total)
    return success_response(message='查询TodoLog列表成功', data=res_data)


# 删除
@router.delete('/delete')
async def delete_todo_log(
        todo_log_id: int = Query(..., alias="todoLogId"),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await todo_log.delete_todo_log(todo_log_id, db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未找到该TodoLog')
    return success_response(message='删除TodoLog成功')


# 更新
@router.put('/update')
async def update_todo_log(
        update_data: TodoLogUpdateRequest = Body(...),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await todo_log.update_todo_log(update_data.model_dump(exclude_none=True, exclude_unset=True), db)
    updated_todo_log = TodoLogItemResponse().model_validate(result)
    return success_response(message='更新TodoLog成功', data=updated_todo_log)
