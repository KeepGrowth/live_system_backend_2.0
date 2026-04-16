from sqlalchemy import func, Date, DateTime, String, Integer, ForeignKey, Text, Index, UniqueConstraint
from typing import Optional, List

from sqlalchemy.orm import relationship

from config.mysql_config import Base, mapped_column, Mapped
from datetime import date, datetime


# Okr基类
class OkrBase(Base):
    __abstract__ = True
    create_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="更新时间")


# OKR类
class Okr(OkrBase):
    __tablename__ = "okr"
    # 创建查询索引

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键")
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户id")
    program_id: Mapped[int] = mapped_column(Integer, ForeignKey('program.id'), nullable=False,
                                            comment="外键-项目id")  # 相当于OKR中的O
    kr_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="okr名称")
    kr_desc: Mapped[str] = mapped_column(Text, nullable=True, comment="okr描述")
    status: Mapped[int] = mapped_column(Integer, default=0, comment="状态,0待完成，1已完成，2已放弃")
    # 联合唯一约束，同一个项目中不能有重复的OKR名称。
    __table_args__ = (
        UniqueConstraint('program_id', 'kr_name', name='uk_program_kr_name'),
    )

    # --- 反向映射关系 ---
    # 一对一关系
    # 一个OKR只能对应一个项目
    program: Mapped["Program"] = relationship("Program", back_populates="okrs", foreign_keys=[program_id])

    # 一对多关系
    # 一个OKR对应多个todo
    todos: Mapped[List["Todo"]] = relationship("Todo", back_populates="okr", lazy="dynamic")
    # 一个OKR对应多个todo_log
    todo_logs: Mapped[List["TodoLog"]] = relationship("TodoLog", back_populates="okr", lazy="dynamic")
    # 一个OKR对应多张图片
    upload_images: Mapped[List["UploadImages"]] = relationship("UploadImages", back_populates="okr", lazy="dynamic")
