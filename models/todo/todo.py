from sqlalchemy import func, Date, DateTime, String, Integer, ForeignKey, Text, Index, UniqueConstraint
from typing import Optional, List

from sqlalchemy.orm import relationship

from config.mysql_config import Base, mapped_column, Mapped
from datetime import date, datetime


# todo基类
class TodoBase(Base):
    __abstract__ = True
    create_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="更新时间",onupdate=datetime.now, )


# todo类
class Todo(TodoBase):
    __tablename__ = "todo"

    # 基础信息
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="todo id")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment="外键关联-用户id")
    title: Mapped[str] = mapped_column(String(150), nullable=False, comment="todo标题")
    todo_goal: Mapped[str] = mapped_column(Text, nullable=True, comment="todo目标，此待办需要完成的目标")
    finish_desc: Mapped[str] = mapped_column(Text, nullable=True, comment="完成描述")
    quit_desc: Mapped[str] = mapped_column(Text, nullable=True, comment="放弃描述")
    importance: Mapped[int] = mapped_column(Integer, nullable=True, default=0,
                                            comment="todo重要程度：0不紧急不重要，1不紧急重要，2不紧急不重要，3紧急重要")
    status: Mapped[int] = mapped_column(Integer, nullable=True, default=0,
                                        comment="todo状态：0待完成，1进行中，2已完成,3已放弃")
    focus_time: Mapped[int] = mapped_column(Integer, nullable=True, default=0, comment="todo专注时间(分钟)")
    deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="todo截止日期")
    emotion: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, default=0,
                                                   comment="todo心情：由AI预测的文本")

    # 联表信息
    goal_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('goal.id'), nullable=True,
                                                   comment="外键关联-目标id")
    program_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('program.id'), nullable=True,
                                                      comment="外键关联-项目id")
    okr_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('okr.id'), nullable=True,
                                                  comment="外键关联-OKR id")

    # --- 反向映射关系 ---
    # 一个todo对应一个用户
    user: Mapped["User"] = relationship("User", back_populates="todos", foreign_keys=[user_id], lazy="selectin")
    # 一个todo对应一个okr
    okr: Mapped["Okr"] = relationship("Okr", back_populates="todos", foreign_keys=[okr_id], lazy="selectin")
    # 一个todo对应一个项目
    program: Mapped["Program"] = relationship("Program", back_populates="todos", foreign_keys=[program_id], lazy="selectin")
    # 一个todo对应一个目标
    goal: Mapped["Goal"] = relationship("Goal", back_populates="todos", foreign_keys=[goal_id], lazy="selectin")
    # 一个todo对应多个todo日志
    todo_logs: Mapped[List["TodoLog"]] = relationship("TodoLog", back_populates="todo", lazy="selectin")
    # 一个todo对应多个图片
    upload_images: Mapped[List["UploadImages"]] = relationship("UploadImages", back_populates="todo", lazy="selectin")

    # -------------------- 标签映射方法 --------------------
    @property
    def status_label(self) -> str:
        """
        todo状态标签
        :return:
        """
        if self.status == 0:
            return "待完成"
        elif self.status == 1:
            return "进行中"
        elif self.status == 2:
            return "已完成"
        elif self.status == 3:
            return "已放弃"
        else:
            return "未知"

    @property
    def importance_label(self) -> str:
        """
        todo重要程度标签
        :return:
        """
        if self.importance == 0:
            return "紧急不重要"
        elif self.importance == 1:
            return "紧急重要"
        elif self.importance == 2:
            return "不紧急不重要"
        elif self.importance == 3:
            return "不紧急重要"
        else:
            return "未知"
