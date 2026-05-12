from sqlalchemy import func, Date, DateTime, String, Integer, ForeignKey, Text, Index, Float
from typing import Optional, List

from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date, datetime

from models.base import Base


# 项目映射类基类
class IncomeBase(Base):
    __abstract__ = True
    create_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="更新时间",
                                                  onupdate=datetime.now(), )


# 收入类
class Income(IncomeBase):
    __tablename__ = "income"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="收入id")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment="外键关联-用户id")
    first_cate_id: Mapped[int] = mapped_column(Integer, ForeignKey('income_cate.id'), nullable=False,
                                               comment="外键关联-收入一级分类id")
    second_cate_id: Mapped[int] = mapped_column(Integer, ForeignKey('income_second_cate.id'), nullable=False,
                                                comment="外键关联-收入二级分类id")
    amount: Mapped[float] = mapped_column(Float, nullable=False, comment="收入金额")
    income_date: Mapped[date] = mapped_column(Date, nullable=False, comment="收入时间")
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="收入备注")

    # 2. 定义 Property
    @property
    def first_cate_name(self) -> str:
        """获取一级分类名称"""
        # 检查关联对象是否存在，防止报错
        if self.first_cate:
            return self.first_cate.first_cate_name  # 假设分类表里的名称字段叫 name
        return ""

    @property
    def second_cate_name(self) -> str:
        """获取二级分类名称"""
        # 检查关联对象是否存在，防止报错
        if self.second_cate:
            return self.second_cate.second_cate_name  # 假设分类表里的名称字段叫 name
        return ""

    # --- 反向映射关系 ---

    # 一对一关系
    # 关联用户
    user: Mapped["User"] = relationship("User", back_populates="incomes", foreign_keys=[user_id])
    first_cate: Mapped["IncomeCate"] = relationship("IncomeCate", back_populates="incomes",
                                                    foreign_keys=[first_cate_id])
    second_cate: Mapped["IncomeSecondCate"] = relationship("IncomeSecondCate", back_populates="incomes",
                                                           foreign_keys=[second_cate_id])

    # 一对多关系
    # 关联图片
    upload_images: Mapped[List["UploadImages"]] = relationship("UploadImages", back_populates="income")


# 收入一级分类
class IncomeCate(IncomeBase):
    __tablename__ = "income_cate"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="收入一级分类id")
    first_cate_name: Mapped[str] = mapped_column(String(50), nullable=False, comment="收入一级分类名称")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment="外键关联-用户id")

    incomes: Mapped[List["Income"]] = relationship("Income", back_populates="first_cate",
                                                   foreign_keys=[Income.first_cate_id])


# 收入二级分类
class IncomeSecondCate(IncomeBase):
    __tablename__ = "income_second_cate"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="收入二级分类id")
    second_cate_name: Mapped[str] = mapped_column(String(50), nullable=False, comment="收入二级分类名称")
    first_cate_id: Mapped[int] = mapped_column(Integer, ForeignKey('income_cate.id'), nullable=False,
                                               comment="外键关联-收入一级分类id")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment="外键关联-用户id")
    incomes: Mapped[List["Income"]] = relationship("Income", back_populates="second_cate",
                                                   foreign_keys=[Income.second_cate_id])
    __table_args__ = (
        # 收入一级分类索引
        Index('idx_income_first_cate_id', 'first_cate_id'),
    )
