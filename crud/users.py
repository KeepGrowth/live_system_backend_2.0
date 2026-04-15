# 1. 创建用户
from typing import List, Optional

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from schemas.users import UserCreate, UserUpdate
from utils import security
from utils.security import verify_password


# 1. 创建用户
async def create_user(db: AsyncSession, user: dict) -> User:
    user['password'] = security.get_password_hash(user['password'])
    db_user = User(
        **user
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


# 2. 根据ID查询用户
async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


# 3. 根据用户名查询用户
async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


# 4. 根据手机号查询用户
async def get_user_by_phone(db: AsyncSession, phone: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.phone == phone))
    return result.scalar_one_or_none()


# 查询所有用户
async def get_all_users(
        db: AsyncSession
):
    result = await db.execute(select(User))
    return result.scalars().all()


# 5. 查询所有用户（分页）
async def get_users(
        db: AsyncSession,
        page: int = 1,
        page_size: int = 10,
        role: int = None,
        username: str = None
):
    """
    分页条件查询用户
    :param db:
    :param page:
    :param page_size:
    :param role: 角色
    :param username: 用户名
    :return:
    """
    query = select(User)
    if role:
        query = query.where(User.role == role)
    if username:
        query = query.where(User.username.like(f"%{username}%"))
    result = await db.execute(query.offset((page - 1) * page_size).limit(page_size))
    total_query = select(func.count(User.user_id)).select_from(User)
    total = await db.execute(total_query)
    return total.scalar_one(), result.scalars().all()


# 6. 更新用户信息
async def update_user(db: AsyncSession, user_id: int, user_update: dict) -> Optional[User]:
    # 1. 构建更新语句
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(**user_update)  # 将字典解包为 key=value 的形式
        .execution_options(synchronize_session="fetch")  # 确保 session 中的对象也被更新
    )

    # 2. 执行更新
    result = await db.execute(stmt)

    # 3. 检查是否匹配到用户
    if result.rowcount == 0:
        return None

    # 4. 提交事务
    await db.commit()

    # 5. 重新查询并返回更新后的对象 (或者利用 synchronize_session 直接返回 db_user)
    return await get_user_by_id(db, user_id)


# 7. 删除用户
async def delete_user(db: AsyncSession, user_id: int) -> bool:
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        return False

    await db.delete(db_user)
    await db.commit()
    return True


# 8. 用户登录
async def login(db: AsyncSession, username: str, password: str) -> Optional[User]:
    db_user = await get_user_by_username(db, username)
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return db_user


# 9. 更新用户头像
async def update_user_avatar(db: AsyncSession, user_id: int, avatar: str) -> Optional[User]:
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        return None
    db_user.avatar = avatar
    await db.commit()
    await db.refresh(db_user)
    return db_user
