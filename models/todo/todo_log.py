from sqlalchemy import func, Date, DateTime, String, Integer, ForeignKey, Text, Index, UniqueConstraint
from typing import Optional, List

from sqlalchemy.orm import relationship

from config.mysql_config import Base, mapped_column, Mapped
from datetime import date, datetime


# todo_log基类
class TodoLogBase(Base):
    __abstract__ = True
    create_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="更新时间")


# todo_log类
class TodoLog(TodoLogBase):
    __tablename__ = "todo_log"

    # 基础信息
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="todo日志 id")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment="外键关联-用户id")
    todo_id: Mapped[int] = mapped_column(Integer, ForeignKey('todo.id'), nullable=False, comment="外键关联-todo id")
    goal_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('goal.id'), nullable=True,
                                                   comment="外键关联-目标id")
    program_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('program.id'), nullable=True,
                                                      comment="外键关联-项目id")
    okr_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('okr.id'), nullable=True,
                                                  comment="外键关联-OKR id")

    title: Mapped[str] = mapped_column(String(50), nullable=False, comment="todo日志标题")
    score: Mapped[int] = mapped_column(Integer, nullable=True, default=0, comment="满意度评分-满分5分")
    log_desc: Mapped[str] = mapped_column(Text, nullable=True, comment="todo日志描述")
    emotion: Mapped[str] = mapped_column(String(50), nullable=True, comment="心情,由AI-agent预测得到的文本")
    # 附件存储路径
    attachment_path: Mapped[str] = mapped_column(Text, nullable=True, comment="todo日志附件")

    # --- 反向映射关系 ---
    # 一个todo_log对应一个todo
    todo: Mapped["Todo"] = relationship("Todo", back_populates="todo_logs", foreign_keys=[todo_id])
    # 一个todo_log对应一个OKR
    okr: Mapped["Okr"] = relationship("Okr", back_populates="todo_logs", foreign_keys=[okr_id])
    # 一个todo_log对应一个项目
    program: Mapped["Program"] = relationship("Program", back_populates="todo_logs", foreign_keys=[program_id])
    # 一个todo_log对应一个目标
    goal: Mapped["Goal"] = relationship("Goal", back_populates="todo_logs", foreign_keys=[goal_id])
    # 一个todo_log对应一个用户
    user: Mapped["User"] = relationship("User", back_populates="todo_logs", foreign_keys=[user_id])
    # 一个todo_log拥有多张图片
    upload_images: Mapped[List["UploadImages"]] = relationship("UploadImages", back_populates="todo_log", )
