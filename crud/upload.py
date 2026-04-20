# 1. 创建用户
from typing import List, Optional

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from crud.users import get_user_by_id
from models.upload_images import UploadImages
from schemas.users import UserCreate, UserUpdate
from utils import security, sql
from utils.security import verify_password


# 新增
async def add_image(db: AsyncSession, image_params: dict, image_url: str):
    """
    新增图片记录
    :param db:
    :param image_url:
    :return:
    """
    user = await get_user_by_id(db, image_params['user_id'])
    if not user.id:
        return None
    new_image = UploadImages(**image_params,
                             image_url=image_url)
    db.add(new_image)
    await db.commit()
    await db.refresh(new_image)
    return new_image


# 获取总数

async def get_total_list(db: AsyncSession,
                         user_id: int):
    """
    获取某用户上传图像的总数
    :param db:
    :param user_id:
    :return:
    """
    return await sql.get_total_list(db, user_id, UploadImages)
