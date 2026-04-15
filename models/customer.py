from sqlalchemy import func, Date, DateTime, String, Integer, ForeignKey, Text, Index, Double
from typing import Optional
from config.mysql_config import Base, mapped_column, Mapped
from datetime import date, datetime


# 客户信息基类
class CustomerBase(Base):
    __abstract__ = True
    create_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="更新时间")


# 客户行业表
class CustomerField(CustomerBase):
    __tablename__ = "customer_field"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="客户行业id")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment="外键关联-用户id")
    field_name: Mapped[Optional[str]] = mapped_column(String(50), unique=True, comment="客户行业名称")
    field_desc: Mapped[str] = mapped_column(Text, nullable=True, default="待完善", comment="客户行业描述")


# 客户信息表
class Customer(CustomerBase):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="客户id")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment="外键关联-用户id")
    customer_name: Mapped[Optional[str]] = mapped_column(String(255), unique=False, comment="客户名称")
    customer_desc: Mapped[str] = mapped_column(Text, nullable=True, default="待完善", comment="客户描述")
    link_way: Mapped[str] = mapped_column(String(255), default="待完善", comment="联系方式")
    img_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="客户图片|头像路径")
    degree: Mapped[int] = mapped_column(Integer, nullable=True, default=0,
                                        comment="客户等级：0普通客户，1重要客户，2重要客户")
    gender: Mapped[int] = mapped_column(Integer, nullable=True, default=0, comment="客户性别：0未知，1男，2女")
    customer_field_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('customer_field.id'), nullable=True,
                                                             comment="外键关联-客户行业id")
