from sqlalchemy import func, Date, DateTime, String, Integer, ForeignKey
from typing import Optional
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