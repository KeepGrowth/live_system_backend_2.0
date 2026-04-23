from sqlalchemy import func, Date, DateTime, String, Integer, ForeignKey, Text, Index
from typing import Optional, List

from sqlalchemy.orm import relationship

from config.mysql_config import Base, mapped_column, Mapped
from datetime import date, datetime


# 项目映射类基类
class ProgramBase(Base):
    __abstract__ = True
    create_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="更新时间",onupdate=datetime.now, )


# 项目类
class Program(ProgramBase):
    __tablename__ = "program"
    # 创建查询索引
    __table_args__ = (
        # 项目名称索引
        Index('idx_program_name', 'program_name'),
        # 目标id索引
        Index('idx_goal_id', 'goal_id'),
        # 项目状态索引
        Index('idx_program_status', 'program_status'),
        # 项目id索引
        Index('idx_program_id', 'id'),
        # 项目创建时间索引
        Index('idx_program_create_time', 'create_time'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="项目id")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment="外键关联-用户id")
    program_name: Mapped[Optional[str]] = mapped_column(String(50), unique=False, comment="项目名称")
    goal_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('goal.id'), nullable=True,
                                                   comment="外键关联-目标id")
    program_desc: Mapped[str] = mapped_column(Text, default="待完善", comment="项目描述|预期达成结果")
    program_status: Mapped[int] = mapped_column(Integer, default=0, comment="项目状态：0待完成，1进行中，2已完成,3已放弃")
    attachment_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="项目附件路径")
    # 项目满意度评分
    satisfaction_score: Mapped[int] = mapped_column(Integer, default=0, comment="项目满意度评分-满分5分")
    # 预估完成时间
    estimate_finish_time: Mapped[Optional[date]] = mapped_column(Date, nullable=True,
                                                                 comment="项目预估完成时间")
    # 预估开始时间
    estimate_start_time: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="项目预估开始时间")

    # --- 反向映射关系 ---
    # 一对一关系
    # 关联用户
    user: Mapped["User"] = relationship("User", back_populates="programs", foreign_keys=[user_id])
    # 关联目标
    goal: Mapped["Goal"] = relationship("Goal", back_populates="programs", foreign_keys=[goal_id])
    # 关联完成日志
    program_log: Mapped["ProgramLog"] = relationship("ProgramLog", back_populates="program")

    # 一对多关系
    # 关联图片
    upload_images: Mapped[List["UploadImages"]] = relationship("UploadImages", back_populates="program")
    # 关联okr
    okrs: Mapped[List["Okr"]] = relationship("Okr", back_populates="program")
    # 关联todo
    todos: Mapped[List["Todo"]] = relationship("Todo", back_populates="program")
    # 关联todo日志
    todo_logs: Mapped[List["TodoLog"]] = relationship("TodoLog", back_populates="program")


# 项目完成日志
class ProgramLog(ProgramBase):
    __tablename__ = "program_log"
    # 创建查询索引
    __table_args__ = (
        # 项目id索引
        Index('idx_program_id', 'program_id'),
        # 项目完成日志id索引
        Index('idx_finish_program_log_id', 'id'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="项目完成日志id")
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('user.id'), nullable=True,
                                                   comment="外键关联-用户id")
    program_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('program.id'), nullable=True,
                                                      comment="外键关联-项目id")
    description: Mapped[str] = mapped_column(Text, nullable=True, comment="项目日志描述", default="")
    emotion: Mapped[str] = mapped_column(String(50), nullable=True, comment="项目日志心情-AI预测")
    attachment_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="项目日志附件路径")

    # --- 反向映射关系 ---
    # 一对一关系
    # 关联项目
    program: Mapped["Program"] = relationship("Program", back_populates="program_log", foreign_keys=[program_id],
                                              lazy="selectin")
    # 关联用户
    user: Mapped["User"] = relationship("User", back_populates="program_log")
