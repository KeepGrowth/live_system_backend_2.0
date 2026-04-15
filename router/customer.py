from fastapi import HTTPException
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud import customer
from models.users import User
from schemas.customer import CustomerAddRequest, CustomerUpdateRequest, CustomerListResponse, CustomerItemResponse
from models.customer import Customer
from utils.auth import get_current_user
from utils.response import success_response

# 创建api-router实例
router = APIRouter(
    prefix='/api/customer',
    tags=['customer'],
)


# 新增客户
@router.post('/add')
async def add_customer(
        customer_data: CustomerAddRequest,
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await customer.add_customer(db=db, user_id=current_user.id, customer_data=customer_data.model_dump())
    res_data = CustomerItemResponse().model_validate(result)
    return success_response(message="新增客户成功", data=res_data)


# 更新客户
@router.post('/update')
async def update_customer(
        customer_data: CustomerUpdateRequest,
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    result = await customer.update_customer(db=db, customer_id=customer_data.id,
                                            customer_data=customer_data.model_dump())
    res_data = CustomerItemResponse().model_validate(result)
    return success_response(message="更新客户成功", data=res_data)


# 获取客户列表
@router.get('/list')
async def get_customer_list(
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user),
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, ge=1, le=100, description="每页数量")
):
    total, result = await customer.get_customer_list(db=db, user_id=current_user.id, page=page, page_size=page_size)
    customer_list = [CustomerItemResponse().model_validate(item) for item in result]
    has_more = True if len(customer_list) >= page_size else False
    res_data = CustomerListResponse(total=total, customer_list=customer_list, has_more=has_more)
    return success_response(message="获取客户列表成功", data=res_data)


# 删除客户
@router.delete('/delete')
async def delete_customer(
        customer_id: int,
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    row_count = await customer.delete_customer(db=db, customer_id=customer_id)
    return success_response(message=f"删除{row_count}位客户成功", data=row_count)
