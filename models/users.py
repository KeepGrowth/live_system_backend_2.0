from sqlalchemy import func, Date, DateTime, String, Integer, ForeignKey, Text
from typing import Optional, List

from sqlalchemy.orm import relationship

from config.mysql_config import Base, mapped_column, Mapped
from datetime import date, datetime


# 用户映射类基类
class UserBase(Base):
    __abstract__ = True
    create_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="更新时间")


# 用户类
class User(UserBase):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="用户id")
    birthday: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="生日")
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="用户名")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码")
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="邮箱")
    gender: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0,
                                                  comment="性别： 0保密，1男，2女")  # 0保密，1男，2女
    # 头像URL
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="头像URL")
    # 角色
    role: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0, comment="角色：0普通用户，1管理员")
    # 状态
    status: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0, comment="状态：0禁用，1正常")
    # 状态描述（如果被禁用，这里要填充禁用说明。）
    status_desc: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="状态描述")
    # 个性签名
    signature: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="个性签名")
    # 职业
    occupation: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="职业")
    # 所在行业
    industry: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="所在行业")
    # 所在城市
    city: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="所在城市")

    # --- 反向映射关系 ---
    # 一个用户发布多个项目
    programs: Mapped[List["Program"]] = relationship("Program", back_populates="user", lazy="dynamic")

    # 一个用户发布多个目标
    goals: Mapped[List["Goal"]] = relationship("Goal", back_populates="user", lazy="dynamic")
