from fastapi import HTTPException, Path
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud import okr, upload
from crud.todo import todo, todo_log
from models.users import User
from schemas.okr import *
from utils.auth import get_current_user
from utils.common import convert_to_year_program_okr_options
from utils.response import Result
from crud.program import program

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

    # 同步更新todo、todo_log、图片附件
    todo_records = await todo.get_todo_by_okr_id(result.id, db)
    for todo_record in todo_records:
        todo_record.okr_id = result.id
        todo_record.program_id = result.program_id
        todo_record.goal_id = result.goal_id
        await todo.update_todo(todo_record.__dict__, db)

    todo_log_records = await todo_log.get_log_by_okr_id(result.id, db)
    for todo_log_record in todo_log_records:
        todo_log_record.okr_id = result.id
        todo_log_record.program_id = result.program_id
        todo_log_record.goal_id = result.goal_id
        await todo_log.update_todo_log(todo_log_record.__dict__, db)
    upload_images = await upload.get_upload_by_okr_id(result.id, db)
    for upload_image in upload_images:
        upload_image.okr_id = result.id
        upload_image.program_id = result.program_id
        upload_image.goal_id = result.goal_id
        await upload.update_upload(upload_image.__dict__, db)
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
    result = await okr.query_okr_cascade_list(db, current_user_id)
    result = convert_to_year_program_okr_options(result)
    return Result.success(data=result)
