from fastapi import HTTPException
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud import users
from crud.users import login, get_user_by_username, create_user, get_user_by_phone, get_user_by_id
from models.users import User
from schemas.users import *
from utils import security
from utils.auth import get_current_user, create_access_token
from utils.response import Result
from utils.security import verify_password, get_password_hash

# 创建api-router实例
router = APIRouter(
    prefix='/api/user',
    tags=['user'],
)


# ------------------------------
# RESTful API 接口
# ------------------------------
@router.post("/login", summary="用户登录", status_code=status.HTTP_200_OK)
async def login_api(
        user: UserLogin,
        db: AsyncSession = Depends(get_database)
):
    """用户登录"""
    user = await login(db, user.username, user.password)
    if not user:
        return Result.error(code=400, msg="用户名或密码错误")
    token = create_access_token(data={"user_id": user.id})
    res_data = UserTokenResponse(token=token, user_info=SafeUserResponse().model_validate(user))
    return Result.success(data=res_data)


@router.post("/register", summary="用户注册", status_code=status.HTTP_200_OK)
async def register_api(
        user: UserCreate,
        db: AsyncSession = Depends(get_database)
):
    """用户注册"""
    # 唯一性校验
    if await get_user_by_username(db, user.username):
        return Result.error(msg="用户已存在")
    new_user = await create_user(db, user.model_dump(exclude_none=True, exclude_unset=True))
    res_data = SafeUserResponse().model_validate(new_user)
    return Result.success(msg="注册成功，为了方便后续个性化使用，请到个人中心完善您的个人信息。", data=res_data)


# 修改密码接口
@router.put("/pwd", summary="修改密码", status_code=status.HTTP_200_OK)
async def update_pwd_api(
        pwd_info: PwdUpdate,
        db: AsyncSession = Depends(get_database),
        # 假设 get_current_user 返回的是用户的 ID (int)
        current_user_id: int = Depends(get_current_user)
):
    """
    修改密码接口
    """
    # 1. 获取当前用户
    # 注意：这里需要确保 user 存在，get_user_by_id 如果没找到应该抛出 HTTPException 或返回 None
    user = await users.get_user_by_id(db, current_user_id)  # 假设你有一个通用的 crud 方法

    if not user:
        return Result.error(msg="用户不存在", code=404)

    # 2. 验证旧密码
    if not verify_password(pwd_info.old_password, user.password):
        return Result.error(msg="旧密码错误")

    # 3. 检查新密码是否与旧密码相同 (可选的安全建议)
    if verify_password(pwd_info.new_password, user.password):
        return Result.error(msg="新密码不能与旧密码相同")

    # 4. 准备更新数据 (不要直接修改 pwd_info)
    # 明确构建更新字典，只包含需要更新的字段
    update_data = {
        "password": get_password_hash(pwd_info.new_password)
    }

    # 5. 执行更新
    try:
        updated_user = await users.update_user(db, user.id, update_data)

        # 6. 构建返回响应
        # 确保 updated_user 是 ORM 对象或字典，能被 SafeUserResponse 解析
        safe_user_info = SafeUserResponse.model_validate(updated_user)

        return Result.success(msg="修改密码成功", data=safe_user_info)

    except Exception as e:
        # 记录日志
        # logger.error(e)
        return Result.error(msg="系统错误，修改密码失败")
