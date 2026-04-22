from fastapi import HTTPException, Path
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud.program import program
from models.users import User
from schemas.program.program import ProgramAddRequest, ProgramItemResponse, ProgramListResponse, ProgramUpdateRequest, \
    ProgramQueryParams
from utils.auth import get_current_user
from utils.common import convert_to_year_program_options
from utils.response import Result

# 创建api-router实例
router = APIRouter(
    prefix='/api/program',
    tags=['program'],
)


# 新增项目
@router.post('/add')
async def add_program(
        add_program_info: ProgramAddRequest,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    add_program_info.user_id = current_user_id
    new_program = await program.add_program(add_program_info.model_dump(exclude_none=True, exclude_unset=True), db)
    return Result.success(data=new_program.id)


# 条件查询分页列表
@router.get('/list')
async def get_program_list(
        query_params: ProgramQueryParams = Query(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user),
):
    """
    条件查询分页项目列表
    :param query_params:
    :param db:
    :param current_user_id:
    :return:
    """
    query_params.user_id = current_user_id
    total, result_list = await program.get_program_list(db=db,
                                                        query_params=query_params.model_dump(exclude_none=True,
                                                                                             exclude_unset=True))
    program_list = [ProgramItemResponse().model_validate(item) for item in result_list]
    if len(program_list) == 0:
        return Result.success(data=[])
    res_data = ProgramListResponse(total=total,
                                   programList=program_list, )
    return Result.success(data=res_data)


# 获取项目详情
@router.get('/detail/{program_id}')
async def get_program_detail(
        program_id: int = Path(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """
    获取项目详情
    :param program_id: 项目id
    :param db:
    :param current_user_id:当前用户id
    :return:
    """
    program_detail = await program.get_program_by_id(db=db, program_id=program_id)
    if program_detail.user_id != current_user_id:
        return Result.error(msg="无访问权限", code=403)
    if not program_detail:
        return Result.error(msg="项目不存在", code=404)
    res_data = ProgramItemResponse().model_validate(program_detail)
    return Result.success(data=res_data)


# 删除项目
@router.delete('/delete/{program_id}')
async def delete_program(
        program_id: int = Path(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """
    根据项目id删除项目
    """
    try:
        target_program = await program.get_program_by_id(db=db, program_id=program_id)
        if target_program.user_id != current_user_id:
            return Result.error(msg="无权限删除项目", code=status.HTTP_403_FORBIDDEN)
        deleted_program_count = await program.delete_program(db=db, program_id=program_id)
        if deleted_program_count == 0:
            return Result.error(msg="项目不存在", code=404)
        return Result.success()
    except Exception as e:
        return Result.error(msg="删除项目失败,该项目含有其他关联数据，请先删除关联数据", code=500)


# 更新项目信息
@router.put('/update')
async def update_program(
        update_program_info: ProgramUpdateRequest,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """
    更新项目信息
    :param update_program_info:更新的项目信息
    :param db:数据库会话
    :param current_user_id:当前用户ID
    :return:RestFul响应
    """
    updated_program = await program.update_program(db=db,
                                                   update_data=update_program_info.model_dump(
                                                       exclude_none=True,
                                                       exclude_unset=True))
    return Result.success()


# 获取项目级联选项
@router.get('/multi-options')
async def get_program_multi_options(
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """
    根据用户ID，获取所有年份的所有项目，更改数据格式为级联选项格式。
    """
    total, result = await program.get_program_list(db, query_params={"user_id": current_user_id})
    program_list = [item.__dict__ for item in result]
    result = convert_to_year_program_options(program_list)
    return Result.success(data=result)
