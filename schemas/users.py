# ------------------------------
# Pydantic 模型（用于接口参数）
# ------------------------------
from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field

from models.users import User


# 用户登录参数
class UserLogin(BaseModel):
    username: str
    password: str
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


class UserCreate(BaseModel):
    username: str
    password: str
    # 角色
    role: Optional[int] = Field(None, alias="role")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


class UserUpdate(BaseModel):
    id: Optional[int] = Field(None, alias="id")
    username: Optional[str] = Field(None, alias="username")
    birthday: Optional[date] = Field(None, alias="birthday")
    email: Optional[str] = Field(None, alias="email")
    gender: Optional[int] = Field(None, alias="gender")
    avatar: Optional[str] = Field(None, alias="avatar")
    role: Optional[int] = Field(None, alias="role")
    status: Optional[int] = Field(None, alias="status")
    status_desc: Optional[str] = Field(None, alias="statusDesc")
    signature: Optional[str] = Field(None, alias="signature")
    occupation: Optional[str] = Field(None, alias="occupation")
    industry: Optional[str] = Field(None, alias="industry")
    city: Optional[str] = Field(None, alias="city")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 修改密码请求
class PwdUpdate(BaseModel):
    old_password: str = Field(None, alias="oldPassword")
    new_password: str = Field(None, alias="newPassword")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 用户安全信息响应
class SafeUserResponse(BaseModel):
    id: int = Field(None, alias="id")
    username: Optional[str] = Field(None, alias="username")
    birthday: Optional[date] = Field(None, alias="birthday")
    email: Optional[str] = Field(None, alias="email")
    gender: Optional[int] = Field(None, alias="gender")
    avatar: Optional[str] = Field(None, alias="avatar")
    role: Optional[int] = Field(None, alias="role")
    status: Optional[int] = Field(None, alias="status")
    status_desc: Optional[str] = Field(None, alias="statusDesc")
    signature: Optional[str] = Field(None, alias="signature")
    occupation: Optional[str] = Field(None, alias="occupation")
    industry: Optional[str] = Field(None, alias="industry")
    city: Optional[str] = Field(None, alias="city")
    create_time: Optional[datetime] = Field(None, alias="createTime")
    update_time: Optional[datetime] = Field(None, alias="updateTime")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 用户列表信息
class UserListResponse(BaseModel):
    total: int = Field(None, alias="total")
    user_list: List[SafeUserResponse] = Field(None, alias="users")


# 用户令牌信息响应
class UserTokenResponse(BaseModel):
    token: str = Field(None, alias="token")
    user_info: SafeUserResponse = Field(None, alias="userInfo")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )
