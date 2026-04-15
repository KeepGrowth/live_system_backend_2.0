from fastapi import HTTPException
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud.program import program
from models.users import User
from schemas.program.program import ProgramAddRequest, ProgramItemResponse, ProgramListResponse, ProgramUpdateRequest
from utils.auth import get_current_user

# 创建api-router实例
router = APIRouter(
    prefix='/api/program',
    tags=['program'],
)


# 新增项目
@router.post('/add')
async def add_program(
        program_data: ProgramAddRequest,
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    new_program = await program.add_program(db=db, user_id=current_user.id, program_name=program_data.program_name)
    res_data = ProgramItemResponse().model_validate(new_program)
    return success_response(message="新增项目成功", data=res_data)


# 获取项目列表
@router.get('/list')
async def get_program_list(
        page: int = Query(1, description="页码"),
        page_size: int = Query(10, description="每页数量", alias="pageSize"),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user),
):
    total, result = await program.get_program_list(db=db, user_id=current_user.id, page=page, page_size=page_size)
    program_list = [ProgramItemResponse().model_validate(r) for r in result]
    has_more = total > page * page_size
    res_data = ProgramListResponse(total=total, program_list=program_list, has_more=has_more)
    return success_response(message="获取项目列表成功", data=res_data)


# 获取项目详情
@router.get('/detail')
async def get_program_detail(
        program_id: int = Query(..., alias="programId", description="项目id"),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    """
    获取项目详情
    :param program_id: 项目id
    :param db:
    :param current_user: 校验token通过的user
    :return:
    """
    program_detail = await program.get_program_detail(db=db, program_id=program_id)
    if not program_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="项目不存在")
    res_data = ProgramItemResponse().model_validate(program_detail)
    return success_response(message="获取项目详情成功", data=res_data)


# 删除项目
@router.delete('/delete')
async def delete_program(
        program_id: int = Query(..., alias="programId", description="项目id"),
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    """
    根据项目id删除项目
    """
    deleted_program_count = await program.delete_program(db=db, program_id=program_id)
    if deleted_program_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="项目不存在")
    return success_response(message=f"用户{current_user.username}删除{deleted_program_count}条项目成功")


# 更新项目信息
@router.put('/update')
async def update_program(
        update_data: ProgramUpdateRequest,
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    """
    更新项目信息
    """
    print(update_data.model_dump())
    updated_program = await program.update_program(db=db, update_data=update_data.model_dump(exclude_none=True,
                                                                                             exclude_unset=True))
    res_data = ProgramItemResponse().model_validate(updated_program)
    return success_response(message="更新项目信息成功", data=res_data)
