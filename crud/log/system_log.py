import datetime
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from models.log.system_log import SystemLog


# 新增
async def add_log(
        system_log_info: dict,
        db: AsyncSession,
):
    new_system_log = SystemLog(**system_log_info)
    db.add(new_system_log)
    await db.commit()
    await db.refresh(new_system_log)
    return new_system_log
