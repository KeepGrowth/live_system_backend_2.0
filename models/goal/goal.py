from sqlalchemy import func, Date, DateTime, String, Integer, ForeignKey, Text, Index
from typing import Optional, List

from sqlalchemy.orm import relationship

from config.mysql_config import Base, mapped_column, Mapped
from datetime import date, datetime


# 目标映射类基类
class GoalBase(Base):
    __abstract__ = True
    create_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="更新时间")


# 目标分类表
class GoalCategory(GoalBase):
    __tablename__ = "goal_category"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="目标分类id")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment="外键关联-用户id")
    category_name: Mapped[str] = mapped_column(String(50), comment="目标分类名称")
    description: Mapped[str] = mapped_column(Text, default="待完善", comment="目标分类描述")

    # --- 反向映射关系 ---
    # 一个目标分类下有多个目标
    goals: Mapped[List["Goal"]] = relationship("Goal", back_populates="goal_category", lazy="dynamic")


# 目标映射类
class Goal(GoalBase):
    __tablename__ = "goal"

    __table_args__ = (
        # 目标名称索引
        Index('idx_goal_name', 'goal_name'),
        # 目标id索引
        Index('idx_goal_id', 'id'),
        # 目标完成时间索引
        Index('idx_goal_finish_time', 'finish_date'),
        # 目标创建时间索引
        Index('idx_goal_create_time', 'create_time'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="目标id")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment="外键关联-用户id")
    goal_name: Mapped[str] = mapped_column(String(50), comment="目标名称")
    description: Mapped[str] = mapped_column(Text, nullable=True, default="待完善", comment="目标描述|预期达成结果")
    # 目标分类id
    goal_category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('goal_category.id'), nullable=True,
                                                            comment="外键-目标分类id")
    # 目标结束状态：0待完成，1进行中，2已完成,3已放弃
    goal_status: Mapped[int] = mapped_column(Integer, nullable=True, default=0,
                                             comment="目标状态：0待完成，1进行中，2已完成,3已放弃")
    # 目标完成情况满意度评分
    satisfaction_score: Mapped[int] = mapped_column(Integer, nullable=True, default=0,
                                                    comment="目标计划满意度评分-满分5分")
    # 目标计划开始时间
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="目标计划开始时间")
    # 目标计划完成时间
    finish_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="目标完成时间")

    # --- 反向映射关系 ---
    # 一对一关系
    # 一个目标智能一个用户拥有
    user: Mapped["User"] = relationship("User", back_populates="goals", foreign_keys=[user_id], lazy="dynamic")

    # 一个目标只能有一个目标分类
    goal_category: Mapped["GoalCategory"] = relationship("GoalCategory", back_populates="goals",
                                                         foreign_keys=[goal_category_id])

    # 一对多关系
    # 一个目标有多个项目
    programs: Mapped[List["Program"]] = relationship("Program", back_populates="goal", lazy="dynamic")
    # 一个目标有多个OKR
    okrs: Mapped[List["Okr"]] = relationship("OKR", back_populates="goal", lazy="dynamic")
    # 一个目标有多个todo日志
    todo_logs: Mapped[List["TodoLog"]] = relationship("TodoLog", back_populates="goal", lazy="dynamic")
    # 一个目标有多个todo
    todos: Mapped[List["Todo"]] = relationship("Todo", back_populates="goal", lazy="dynamic")
    # 一个目标有多张图片
    upload_images: Mapped[List["UploadImages"]] = relationship("UploadImages", back_populates="goal", lazy="dynamic")
