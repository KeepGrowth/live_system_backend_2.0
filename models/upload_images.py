from sqlalchemy import func, Date, DateTime, String, Integer, ForeignKey, Text, Index, UniqueConstraint
from typing import Optional

from sqlalchemy.orm import relationship

from config.mysql_config import Base, mapped_column, Mapped
from datetime import date, datetime


# 图床基类
class UploadBase(Base):
    __abstract__ = True
    create_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")


# 图床类
class UploadImages(UploadBase):
    __tablename__ = "upload_images"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="主键")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment="用户id")
    todo_log_id: Mapped[int] = mapped_column(Integer, ForeignKey('todo_log.id'), nullable=True,
                                             comment="外键-todo_log_id")
    todo_id: Mapped[int] = mapped_column(Integer, ForeignKey('todo.id'), nullable=True, comment="外键-todo_id")
    okr_id: Mapped[int] = mapped_column(Integer, ForeignKey('okr.id'), nullable=True, comment="外键-okr_id")
    program_id: Mapped[int] = mapped_column(Integer, ForeignKey('program.id'), nullable=True, comment="外键-项目id")
    goal_id: Mapped[int] = mapped_column(Integer, ForeignKey('goal.id'), nullable=True, comment="外键-目标id")
    image_url: Mapped[str] = mapped_column(Text, nullable=False, comment="图片URL")

    # --- 反向映射关系 ---
    # 一个图片对应一个用户
    user: Mapped["User"] = relationship("User", back_populates="upload_images", foreign_keys=[user_id])
    # 一个图片对应一个todo日志
    todo_log: Mapped["TodoLog"] = relationship("TodoLog", back_populates="upload_images", foreign_keys=[todo_log_id],
                                               lazy="selectin")
    # 一个图片对应一个todo
    todo: Mapped["Todo"] = relationship("Todo", back_populates="upload_images", foreign_keys=[todo_id])
    # 一个图片对应一个okr
    okr: Mapped["Okr"] = relationship("Okr", back_populates="upload_images", foreign_keys=[okr_id])
    # 一个图片对应一个项目
    program: Mapped["Program"] = relationship("Program", back_populates="upload_images", foreign_keys=[program_id],
                                              lazy="selectin")
    # 一个图片对应一个目标
    goal: Mapped["Goal"] = relationship("Goal", back_populates="upload_images", foreign_keys=[goal_id])

    # ----------- 标签映射方法 -----------
    @property
    def create_time_str(self):
        return self.create_time.strftime("%Y-%m-%d %H:%M:%S")
