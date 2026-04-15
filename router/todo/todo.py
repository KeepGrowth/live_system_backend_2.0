from fastapi import HTTPException, Body
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud.todo import todo
from models.todo.todo import Todo
from models.users import User
from schemas.todo.todo import *
from utils.auth import get_current_user

router = APIRouter(
    prefix='/api/todo',
    tags=['todo'],
)


@router.post('/add')
async def add_todo(
        add_data: TodoAddRequest = Body(...),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await todo.add_todo(add_data.model_dump(exclude_none=True, exclude_unset=True), db, current_user.id)
    new_todo = TodoItemResponse().model_validate(result)
    return success_response(message='新增Todo成功', data=new_todo)


# 条件查询todo列表
@router.get('/list')
async def get_todo_list(
        filter_data: TodoQueryRequest = Query(...),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    print("1111", filter_data.model_dump())
    total, result = await todo.query_todo_list(db=db,
                                               user_id=current_user.id,
                                               filter_data=filter_data.model_dump(exclude_none=True,
                                                                                  exclude_unset=True))
    todo_list = [TodoItemResponse().model_validate(r) for r in result]
    res_data = TodoListResponse(todo_list=todo_list, total=total)
    return success_response(message='获取Todo列表成功', data=res_data)


@router.put('/update')
async def update_todo(
        update_data: TodoUpdateRequest,
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await todo.update_todo(update_data.model_dump(exclude_none=True, exclude_unset=True), db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未找到该Todo')
    updated_todo = TodoItemResponse().model_validate(result)
    return success_response(message='更新Todo成功', data=updated_todo)


@router.delete('/delete')
async def delete_todo(
        todo_id: int = Query(..., description="Todo id", alias="todoId"),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await todo.delete_todo(todo_id, db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未找到该Todo')
    return success_response(message='删除Todo成功')
