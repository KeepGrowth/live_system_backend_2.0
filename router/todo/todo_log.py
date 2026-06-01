import json

import redis.asyncio as redis
from fastapi import HTTPException, Body, Path
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud import upload
from crud.todo import todo_log
from models.users import User
from schemas.todo.todo_log import *
from utils.auth import get_current_user
from utils.response import Result
from crud.todo.todo import *
from utils import service_utils

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
    todo = await get_todo_by_id(todo_log_info.todo_id, db)
    if todo:
        todo_log_info.okr_id = todo.okr_id
        todo_log_info.program_id = todo.program_id
        todo_log_info.goal_id = todo.goal_id
    result = await todo_log.add_todo_log(todo_log_info.model_dump(exclude_none=True, exclude_unset=True, exclude={
        'image_list'
    }), db)
    # 新增成功后更新对应的图片ID绑定
    if result and todo_log_info.image_list:
        for item in todo_log_info.image_list:
            if item.get('id', None) is None:
                continue
            await upload.update_image(db, item['id'], {
                "image_url": item['url'],
                "todo_log_id": result.id,
                "todo_id": result.todo_id,
                "okr_id": result.okr_id,
                "program_id": result.program_id,
                "goal_id": result.goal_id,
            })
    new_todo_log = TodoLogJoinItemResponse().model_validate(result)
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
    if update_log_info.todo_id:
        todo = await todo_log.get_log_by_todo_id(update_log_info.todo_id,db)
        update_log_info.okr_id = todo.okr_id
        update_log_info.program_id = todo.program_id
        update_log_info.goal_id = todo.goal_id
    result = await todo_log.update_todo_log(update_log_info.model_dump(exclude_none=True, exclude_unset=True), db)
    if not result:
        return Result.error('更新日志失败TodoLog', code=403)

    # 同步更新日志绑定的信息。
    await service_utils.update_todo_log_bind_data(db, result)
    updated_todo_log = TodoLogItemResponse().model_validate(result)
    return Result.success(data=updated_todo_log)


# 通过todo获取log数据
@router.get('/list_by_todo')
async def get_todo_log_list_by_todo(
        todo_id: int = Query(..., alias="todoId"),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """
    通过todo获取log数据
    :param todo_id:
    :param db:
    :param current_user_id:
    :return:
    """
    total, result = await todo_log.query_todo_log_list(db, filter_data={
        "todo_id": todo_id
    })
    todo_log_list = [TodoLogItemResponse().model_validate(r) for r in result]
    res_data = TodoLogListResponse(todo_log_list=todo_log_list, total=total)
    return Result.success(data=res_data)
