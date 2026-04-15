import datetime
import uuid
from fastapi import HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.customer import Customer
from schemas.customer import CustomerAddRequest, CustomerUpdateRequest
from utils import sql


# 新增客户
async def add_customer(
        customer_data: dict,
        db: AsyncSession,
        user_id: int,
):
    new_customer = await sql.add(db, Customer, add_data=customer_data, check_unique=True, user_id=user_id)
    return new_customer


# 获取客户列表
async def get_customer_list(
        db: AsyncSession,
        user_id: int,
        page: int,
        page_size: int,
):
    total, customer_list = await sql.get_list_by_user_id(db, Customer, user_id, page, page_size)
    return total, customer_list


# 更新客户信息
async def update_customer(
        customer_data: dict,
        db: AsyncSession,
        customer_id: int,
):
    updated_customer = await sql.update_by_id(db, Customer, customer_id, **customer_data)
    return updated_customer


# 删除客户信息
async def delete_customer(
        db: AsyncSession,
        customer_id: int,
):
    deleted_customer = await sql.delete_by_id(db, Customer, customer_id)
    return deleted_customer
