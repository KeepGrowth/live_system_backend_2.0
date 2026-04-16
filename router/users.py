from fastapi import HTTPException, Body
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
from utils.common import verify_code
from utils.response import Result
from utils.security import verify_password, get_password_hash
from utils.send_email.generate_code import generate_code
from utils.send_email.send_email import JinjaEmailSender

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


# 用户注册功能
@router.post("/register", summary="用户注册", status_code=status.HTTP_200_OK)
async def register_api(
        user: UserCreate,
        db: AsyncSession = Depends(get_database)
):
    """用户注册"""
    # 校验邮箱验证码。
    is_right = verify_code(user.code, user.email)
    if not is_right:
        return Result.error(code=400, msg="验证码错误或已过期")
    # 唯一性校验
    if await get_user_by_username(db, user.username):
        return Result.error(msg="用户已存在")
    print(user)
    new_user = await create_user(db, user.model_dump(exclude_none=True, exclude_unset=True, exclude={'code'}))
    res_data = SafeUserResponse().model_validate(new_user)
    print(res_data)
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


# 用户修改个人信息接口
@router.put("/info", summary="修改个人信息", status_code=status.HTTP_200_OK)
async def update_info_api(
        info: UserUpdate,
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """
    修改用户个人信息
    :param info:
    :param db:
    :param current_user_id:
    :return:
    """
    updated_user = await users.update_user(db, user_id=info.id,
                                           user_update=info.model_dump(exclude_none=True, exclude_unset=True))
    return Result.success(msg="修改个人信息成功", data=SafeUserResponse().model_validate(updated_user))


# 禁用/解冻用户
@router.put("/disable", summary="禁用/解冻用户", status_code=status.HTTP_200_OK)
async def disable_user_api(
        user_id: int = Query(..., title="用户ID"),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """
    禁用/解冻用户
    :param user_id:
    :param db:
    :param current_user_id:
    :return:
    """
    user = await users.get_user_by_id(db, user_id)
    # 判断用户是否存在
    if not user:
        return Result.error(msg="用户不存在")
    user_role = await users.get_user_by_id(db, current_user_id)
    # 判断权限
    if user_role.role != 1:
        return Result.error(msg="无权限")
    # 判断是否自杀
    if user_id == current_user_id:
        return Result.error(msg="管理员不能对自己执行此操作")
    user.status = 1 if user.status == 0 else 0
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return Result.success(msg="操作成功", data=SafeUserResponse().model_validate(user))
