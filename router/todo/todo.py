import redis.asyncio as redis
from fastapi import HTTPException, Body, Path
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud.todo import todo
from crud.todo.todo import get_todo_by_id
from crud.okr import get_okr_by_id
from models.todo.todo import Todo
from models.users import User
from schemas.todo.todo import *
from utils.auth import get_current_user
from utils.response import Result

router = APIRouter(
    prefix='/api/todo',
    tags=['todo'],
)


@router.post('/add')
async def add_todo(
        add_data: TodoAddRequest,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    if add_data.okr_id:
        okr = await get_okr_by_id(db, add_data.okr_id)
        add_data.program_id = okr.program_id
        add_data.goal_id = okr.goal_id
    result = await todo.add_todo(add_data.model_dump(exclude_none=True, exclude_unset=True), db, current_user_id)
    return Result.success(msg='新增Todo成功', data=result.id)


# 获取待办详情
@router.get('/detail/{todo_id}')
async def get_todo_detail(
        todo_id: int = Path(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """

    :param todo_id:
    :param db:
    :param current_user_id:
    :return:
    """
    result = await todo.get_todo_by_id(todo_id, db)
    if not result:
        return Result.error(msg='未找到该Todo', code=404)
    if result.user_id != current_user_id:
        return Result.error(msg='无此权限', code=403)
    return Result.success(data=TodoItemResponse().model_validate(result))


# 条件查询待办列表
@router.get('/list')
async def get_todo_list(
        filter_data: TodoQueryRequest = Query(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    filter_data.user_id = current_user_id
    total, result = await todo.query_todo_list(db=db,
                                               query_params=filter_data.model_dump(exclude_none=True,
                                                                                   exclude_unset=True))
    for item in result:
        item.focus_time = sum(getattr(log, 'focus_time', 0) or 0 for log in item.todo_logs)
    todo_list = [TodoJoinItemResponse().model_validate(r) for r in result]
    res_data = TodoListResponse(todo_list=todo_list, total=total)
    return Result.success(data=res_data)


@router.put('/update')
async def update_todo(
        update_data: TodoUpdateRequest,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    update_data.user_id = current_user_id
    if update_data.okr_id:
        okr = await get_okr_by_id(db, update_data.okr_id)
        update_data.program_id = okr.program_id
        update_data.goal_id = okr.goal_id
    result = await todo.update_todo(update_data.model_dump(exclude_none=True, exclude_unset=True), db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未找到该Todo')
    updated_todo = TodoItemResponse().model_validate(result)
    return Result.success(data=updated_todo)


@router.delete('/{todo_id}')
async def delete_todo(
        todo_id: int = Path(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    target_todo = await get_todo_by_id(todo_id, db)
    if target_todo.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='无权限删除该Todo')
    result = await todo.delete_todo(todo_id, db)
    return Result.success(data=result)
