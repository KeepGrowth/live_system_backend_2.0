from sqlalchemy import func, Date, DateTime, String, Integer, ForeignKey, Text, Index, UniqueConstraint
from typing import Optional
from config.mysql_config import Base, mapped_column, Mapped
from datetime import date, datetime


# todo基类
class TodoBase(Base):
    __abstract__ = True
    create_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="更新时间")


# todo类
class Todo(TodoBase):
    __tablename__ = "todo"

    # 基础信息
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="todo id")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment="外键关联-用户id")
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="todo名称")
    finish_desc: Mapped[str] = mapped_column(Text, nullable=True, comment="完成描述")
    quit_desc: Mapped[str] = mapped_column(Text, nullable=True, comment="放弃描述")
    importance: Mapped[int] = mapped_column(Integer, nullable=True, default=0,
                                            comment="todo重要程度：0紧急不重要，1紧急重要，2不紧急不重要，3不紧急重要")
    status: Mapped[int] = mapped_column(Integer, nullable=True, default=0,
                                        comment="todo状态：0待完成，1进行中，2已完成,3已放弃")
    focus_time: Mapped[int] = mapped_column(Integer, nullable=True, default=0, comment="todo专注时间(分钟)")
    deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="todo截止时间")

    # 联表信息
    goal_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('goal.id'), nullable=True,
                                                   comment="外键关联-目标id")
    program_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('program.id'), nullable=True,
                                                      comment="外键关联-项目id")
    okr_id = mapped_column(Integer, ForeignKey('okr.id'), nullable=True, comment="外键关联-OKR id")
    # 附件信息
    attachment_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="todo附件路径")
