from fastapi import HTTPException
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud import weight
from models.users import User
from schemas.weight import *
from utils.auth import get_current_user

# 创建api-router实例
router = APIRouter(
    prefix='/api/weight',
    tags=['weight'],
)

