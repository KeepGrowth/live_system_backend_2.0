from fastapi import HTTPException, Body, Path
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud import upload
from crud.finance import expense, expense_cate, expense_second_cate
from crud.okr import get_okr_by_id
from schemas.finance.expense import *
from schemas.finance.expense_cate import ExpenseFirstCateItemResponse, ExpenseFirstCateListResponse
from schemas.finance.expense_second_cate import ExpenseSecondCateItemResponse, ExpenseSecondCateListResponse
from utils.auth import get_current_user
from utils.response import Result

router = APIRouter(
    prefix='/api/expense',
    tags=['expense'],
)


@router.post('/add')
async def add_expense(
        add_data: ExpenseAddRequest,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    if add_data.okr_id:
        okr = await get_okr_by_id(db, add_data.okr_id)
        add_data.program_id = okr.program_id
        add_data.goal_id = okr.goal_id
    result = await expense.add_expense(
        add_data.model_dump(exclude_none=True, exclude_unset=True, exclude={'image_list'}), db, current_user_id)
    # 新增成功后更新对应的图片ID绑定
    if result and add_data.image_list:
        for item in add_data.image_list:
            if item.get('id', None) is None:
                continue
            await upload.update_image(db, item['id'], {
                "image_url": item['url'],
                "okr_id": result.okr_id,
                "program_id": result.program_id,
                "goal_id": result.goal_id,
                "expense_id": result.id
            })
    return Result.success(msg='新增Expense成功', data=result.id)


# 获取expense详情
@router.get('/detail/{expense_id}')
async def get_expense_detail(
        expense_id: int = Path(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """

    :param expense_id:
    :param db:
    :param current_user_id:
    :return:
    """
    result = await expense.get_expense_by_id(expense_id, db)
    if not result:
        return Result.error(msg='未找到该Expense', code=404)
    if result.user_id != current_user_id:
        return Result.error(msg='无此权限', code=403)
    return Result.success(data=ExpenseItemResponse().model_validate(result))


# 条件查询expense列表
@router.get('/list')
async def get_expense_list(
        filter_data: ExpenseQueryParams = Query(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    filter_data.user_id = current_user_id
    total, result = await expense.query_expense_list(db=db,
                                                     query_params=filter_data.model_dump(exclude_none=True,
                                                                                         exclude_unset=True))

    expense_list = [ExpenseJoinItemResponse().model_validate(r) for r in result]
    res_data = ExpenseJoinListResponse(expense_list=expense_list, total=total)
    return Result.success(data=res_data)


@router.put('/update')
async def update_expense(
        update_data: ExpenseUpdateRequest,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    update_data.user_id = current_user_id
    if update_data.okr_id:
        okr = await get_okr_by_id(db, update_data.okr_id)
        update_data.program_id = okr.program_id
        update_data.goal_id = okr.goal_id
    result = await expense.update_expense(update_data.model_dump(exclude_none=True, exclude_unset=True), db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未找到该Expense')
    updated_expense = ExpenseItemResponse().model_validate(result)
    return Result.success(data=updated_expense)


@router.delete('/{expense_id}')
async def delete_expense(
        expense_id: int = Path(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    target_expense = await expense.get_expense_by_id(expense_id, db)
    if target_expense.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='无权限删除该Expense')
    result = await expense.delete_expense(expense_id, db)
    return Result.success(data=result)


# 查询收入一级分类列表
@router.get('/first_cate/list')
async def get_expense_first_cate_list(
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """
    查询收入一级分类列表
    """
    total, result = await expense_cate.query_first_cate_list(db, user_id=current_user_id)
    result_list = [ExpenseFirstCateItemResponse().model_validate(r) for r in result]
    res_data = ExpenseFirstCateListResponse(expense_first_cate_list=result_list, total=total)
    return Result.success(data=res_data)


# 根据一级分类ID查询二级分类列表
@router.get('/second_cate/list/{first_cate_id}')
async def get_expense_second_cate_list(
        first_cate_id: int = Path(...),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """
    根据一级分类ID查询二级分类列表
    """
    total, result = await expense_second_cate.query_second_cate_list(db, user_id=current_user_id,
                                                                     first_cate_id=first_cate_id)
    result_list = [ExpenseSecondCateItemResponse().model_validate(r) for r in result]
    res_data = ExpenseSecondCateListResponse(expense_second_cate_list=result_list, total=total)
    return Result.success(data=res_data)
